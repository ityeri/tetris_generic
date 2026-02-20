import asyncio
import sys
import time
from enum import Enum, auto

from prompt_toolkit import key_binding
from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import OneStyleAndTextTuple, StyleAndTextTuples
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import Container
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Frame

from tetris_generic import TetrisGame, ControlType
from tetris_generic.default_impl import DefaultSpace, DefaultTetrominoSpawner, DEFAULT_SPACE_WIDTH, DEFAULT_SPACE_HEIGHT
from tetris_generic.event import events
from tetris_generic.tetromino import Tetromino
from .formatted_text_surface import FormattedTextSurface
from .key_map import KeyMap


class ExitedReason(Enum):
    GAME_OVER = auto()
    TERMINATED = auto()

class SplashState(Enum):
    DEFAULT = auto()
    CURRENT_STAT = auto()

def draw_tetromino(surface: FormattedTextSurface, tetromino: Tetromino, text: OneStyleAndTextTuple):
    for dy in range(tetromino.type.size):
        for dx in range(tetromino.type.size):
            if tetromino[dx, dy]:
                game_x, game_y = tetromino.x + dx, tetromino.y + dy
                surface_x, surface_y = game_x, surface.height - game_y - 1

                if 0 <= surface_x < surface.width and 0 <= surface_y < surface.height:
                    surface[surface_x, surface_y] = text


class TerminalRunner:
    def __init__(
            self,
            width: int = DEFAULT_SPACE_WIDTH,
            height: int = DEFAULT_SPACE_HEIGHT,
            interval: float = 0.5,
            que_length: int = 10
    ):
        self.space: DefaultSpace = DefaultSpace(width, height)
        self.spawner: DefaultTetrominoSpawner = \
            DefaultTetrominoSpawner(
                space_width=self.space.width,
                space_height=self.space.height,
                que_length=que_length
            )

        self.game: TetrisGame = TetrisGame(
            initial_space=self.space,
            spawner=self.spawner
        )
        self.tick_interval = interval

        self.game.add_listener(events.TetrominoDropEvent, self.on_tetromino_drop)
        self.game.add_listener(events.TetrominoDownCollisionEvent, self.on_tetromino_down_collision)
        self.game.add_listener(events.TetrominoLandingEvent, self.on_tetromino_landing)
        self.game.add_listener(events.PartDeleteEvent, self.on_part_delete)
        self.game.add_listener(events.GameOverEvent, self.on_game_over)

        self.game_surface: FormattedTextSurface = FormattedTextSurface(
            self.space.width, self.space.height, 2, 1
        )
        self.game_frame: Frame = Frame(
            title=lambda: self.current_splash_text,
            body=Window(
                content=FormattedTextControl(self.game_surface.render),
                width=self.game_surface.h_characters,
                height=self.game_surface.v_characters,
                style='bg:#000000'
            )
        )
        self.que_surface: FormattedTextSurface = FormattedTextSurface(
            4, self.spawner.que_length * 4, 2, 1
        )

        self.current_combo: int = 0
        self.previous_combo: int = 0
        self.best_combo: int = 0
        self.total_deleted_parts: int = 0
        self.last_deleted_parts: int | None = None
        self.splash_state: SplashState = SplashState.DEFAULT

        self.current_splash_text: StyleAndTextTuples = [(' ', 'tetris_generic')]

        self.root_container: Container = HSplit([
            Window(),
            VSplit([
                Window(),
                HSplit([
                    Window(),
                    self.game_frame,
                    Window()
                ]),
                HSplit([
                    Window(),
                    Frame(
                        title='next',
                        # width=self.que_surface.h_characters + 2,
                        # height=self.que_surface.v_characters + 2,
                        body=Window(
                            content=FormattedTextControl(self.que_surface.render),
                            width=self.que_surface.h_characters,
                            height=self.que_surface.v_characters,
                            style='bg:#000000'
                        )
                    ),
                    Window()
                ]),
                Window(),
            ]),
            Window(),
        ])

        layout = Layout(self.root_container)
        self.app: Application = Application(layout=layout, full_screen=True)
        self.running: bool = False

        self.last_tick_time: float = -1
        self.next_tick_time: float = -1

        self.key_map = KeyMap(
            self.game,
            key_map={
                ControlType.LEFT: [('a',), (Keys.Left,), ('h',)],
                ControlType.RIGHT: [('d',), (Keys.Right,), ('l',)],
                ControlType.DOWN: [('s',), (Keys.Down,), ('j',)],

                ControlType.DROP: [(' ',), (Keys.Enter,)],

                ControlType.ROTATE_RIGHT: [('w',), (Keys.Up,), ('k',)],
                ControlType.ROTATE_LEFT: [('z',), ('i',)],
            }
        )
        self.key_map.on_key()(lambda control_type: self.flush())

        kb = self.key_map.create_key_bindings()

        @kb.add(Keys.ControlC)
        def on_exit(event: key_binding.KeyPressEvent):
            self.exited_reason = ExitedReason.TERMINATED
            self.stop()

        self.app.key_bindings = kb

        self.exited_reason: ExitedReason | None = None


    def on_tetromino_drop(self, event: events.TetrominoDropEvent):
        self.set_tick_timer(0)

    def on_tetromino_down_collision(self, event: events.TetrominoDownCollisionEvent):
        if event.reason == events.CollisionReason.TICK:
            self.set_tick_timer(self.tick_interval * 1.5)

    def on_tetromino_landing(self, event: events.TetrominoLandingEvent):
        self.previous_combo = self.current_combo
        self.current_combo = 0

    def on_part_delete(self, event: events.PartDeleteEvent):
        self.current_combo = self.previous_combo + 1
        if self.best_combo < self.current_combo:
            self.best_combo = self.current_combo

        self.total_deleted_parts += event.deleted_parts
        self.last_deleted_parts = event.deleted_parts
        self.splash_state = SplashState.CURRENT_STAT
        self.update_splash_text()

    def on_game_over(self, event: events.GameOverEvent):
        self.exited_reason = ExitedReason.GAME_OVER
        self.stop()

    def update_splash_text(self):
        if self.splash_state == SplashState.DEFAULT:
            self.current_splash_text = [('', 'tetris_generic')]
        elif self.splash_state == SplashState.CURRENT_STAT:
            text = []
            if 2 <= self.current_combo:
                text += [
                    ('#33ff33', str(self.current_combo)),
                    ('#cccccc', ' Combo!'),
                ]

            if self.last_deleted_parts == 4:
                text = text + [
                    ('', ' '),
                    ('#ff0000', 'T'),
                    ('#ff7700', 'E'),
                    ('#ffff00', 'T'),
                    ('#77ff00', 'R'),
                    ('#00ff00', 'I'),
                    ('#00ff77', 'S'),
                    ('#00ffff', '!')
                ]

            if 0 < len(text):
                self.current_splash_text = text
        else:
            raise ValueError('?')

    def flush(self):
        self.render_surface()
        self.app.invalidate()


    def render_surface(self):
        for surface_y in range(self.game_surface.height):
            for surface_x in range(self.game_surface.width):
                game_x, game_y = surface_x, self.space.height - surface_y - 1

                cell = self.space[game_x, game_y]
                if cell is not None:
                    r, g, b = self.space[game_x, game_y].get_display_color()
                else:
                    r, g, b = (0, 0, 0)

                self.game_surface[surface_x, surface_y] = (
                    f'bg:#{r:02x}{g:02x}{b:02x}',
                    ' '
                )

        tetromino = self.game.active_tetromino
        r, g, b = tetromino.type.filling_cell.get_display_color()

        draw_tetromino(
            self.game_surface,
            self.game.landed_tetromino,
            (f'bg:#000000 #ff0000', 'x')
        )

        dropped_tetromino = self.space.get_dropped(self.game.active_tetromino)
        draw_tetromino(
            self.game_surface,
            dropped_tetromino,
            (f'bg:#000000 #{r:02x}{g:02x}{b:02x}', ':')
        )

        draw_tetromino(
            self.game_surface,
            tetromino,
            (f'bg:#{r:02x}{g:02x}{b:02x}', ' ')
        )

        self.que_surface.fill((f'bg:#000000', ' '))

        for i, tetromino_type in enumerate(self.spawner.tetromino_que):
            y = (self.spawner.que_length - i - 1) * 4 + (2 - round(tetromino_type.size / 2))
            x = round(self.que_surface.width / 2 - tetromino_type.size / 2)
            r, g, b = tetromino_type.filling_cell.get_display_color()

            draw_tetromino(
                self.que_surface,
                Tetromino(x, y, 0, tetromino_type),
                (f'bg:#{r:02x}{g:02x}{b:02x}', ' ')
            )


    async def run_tick(self):
        while self.running:
            self.last_tick_time = time.time()
            self.set_tick_timer(self.tick_interval)

            self.game.tick() # game.tick includes tick timer setting task
            self.flush()


            while time.time() < self.next_tick_time:
                await asyncio.sleep(0.01)

    def set_tick_timer(self, interval: float):
        self.next_tick_time = self.last_tick_time + interval


    async def start(self):
        self.game.init()
        self.running = True
        app_task = asyncio.create_task(self.app.run_async())
        tick_task = asyncio.create_task(self.run_tick())

        await app_task
        tick_task.cancel()

        self._exit()

    def _exit(self):
        print("Total deleted lines: " + str(self.total_deleted_parts))
        print("Best combo: " + str(self.best_combo))
        if self.exited_reason == ExitedReason.GAME_OVER:
            print("Game Over!")
            print("ㅂㅂ")
        elif self.exited_reason == ExitedReason.TERMINATED:
            print("Terminated by Ctrl C; bye")

    def stop(self):
        self.running = False
        self.app.exit()

    def run(self):
        asyncio.run(self.start())