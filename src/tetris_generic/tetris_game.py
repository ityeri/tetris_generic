from collections.abc import Callable

from tetris_generic.control_type import ControlType
from tetris_generic.event import ListenerManager, Listener
from tetris_generic.event.events import *
from tetris_generic.event.events import TetrisEvent
from tetris_generic.space import Space
from tetris_generic.tetromino import Tetromino
from tetris_generic.tetromino import TetrominoSpawner


class TetrisGame:
    def __init__(self, initial_space: Space, spawner: TetrominoSpawner):
        self.space: Space = initial_space
        self.spawner: TetrominoSpawner = spawner
        self.landed_tetromino: Tetromino | None = None
        self.active_tetromino: Tetromino | None = None
        self._listener_manager: ListenerManager = ListenerManager()

    def init(self):
        self.active_tetromino = self.spawner.next()
        self.landed_tetromino = self.active_tetromino.moved(0, 0, 0)

    def add_listener[T: TetrisEvent](self, event_type: type[T], listener: Listener[T]):
        self._listener_manager.add_listener(event_type, listener)

    def event[T: TetrisEvent](self, event_type: type[T]) -> Callable[[Listener[T]], None]:
        def wrapper(listener: Listener[T]): self.add_listener(event_type, listener)

        return wrapper

    def trigger_control(self, control: ControlType) -> bool:
        if control == ControlType.LEFT:
            moved_tetromino = self.active_tetromino.moved(-1, 0, 0)
            if self.space.is_collision(moved_tetromino):
                return False
            else:
                self.active_tetromino = moved_tetromino
                return True

        elif control == ControlType.RIGHT:
            moved_tetromino = self.active_tetromino.moved(1, 0, 0)
            if self.space.is_collision(moved_tetromino):
                return False
            else:
                self.active_tetromino = moved_tetromino
                return True

        elif control == ControlType.DOWN:
            moved_tetromino = self.active_tetromino.moved(0, -1, 0)
            if self.space.is_collision(moved_tetromino):
                return False
            else:
                self.active_tetromino = moved_tetromino

                next_tetromino = self.active_tetromino.moved(0, -1, 0)
                if self.space.is_collision(next_tetromino):
                    self._listener_manager.call_event(
                        TetrominoDownCollisionEvent(CollisionReason.CONTROL)
                    )

                return True

        elif control == ControlType.ROTATE_LEFT or control == ControlType.ROTATE_RIGHT:
            rotation_dt = -1 if control == ControlType.ROTATE_LEFT else 1

            test_offsets: list[tuple[int, int]] = \
                self.active_tetromino.type.wall_kick_data.get(
                    self.active_tetromino.rotation,
                    self.active_tetromino.rotation + rotation_dt,
                )

            for x_offset, y_offset in test_offsets:
                moved_tetromino = self.active_tetromino.moved(x_offset, y_offset, rotation_dt)
                if not self.space.is_collision(moved_tetromino):
                    self.active_tetromino = moved_tetromino
                    return True

            return True

        elif control == ControlType.DROP:
            dropped_tetromino = self.space.get_dropped(self.active_tetromino)
            self.active_tetromino = dropped_tetromino

            self._listener_manager.call_event(TetrominoDropEvent())

            return True

        else:
            raise ValueError('Control type is invalid')

    def landing_tetromino(self):
        tetromino_size = self.active_tetromino.type.size
        for dy in range(tetromino_size):
            for dx in range(tetromino_size):
                x, y = self.active_tetromino.x + dx, self.active_tetromino.y + dy

                if self.active_tetromino[dx, dy]:
                    self.space[x, y] = self.active_tetromino.type.filling_cell

    def tick(self):
        moved_tetromino = self.active_tetromino.moved(0, -1, 0)

        if self.space.is_collision(moved_tetromino):
            self.landing_tetromino()
            before_tetromino = self.active_tetromino

            if self.space.is_collision(self.landed_tetromino):
                self._listener_manager.call_event(GameOverEvent())
                self._listener_manager.call_event(TetrominoLandingEvent(
                    before_tetromino=before_tetromino,
                    after_tetromino=None
                ))

                self.active_tetromino = None

            else:
                self.active_tetromino = self.spawner.next()
                self.landed_tetromino = self.active_tetromino.moved(0, 0, 0)

                self._listener_manager.call_event(TetrominoLandingEvent(
                    before_tetromino=before_tetromino,
                    after_tetromino=self.active_tetromino
                ))

                parts = self.space.check_completed_parts()
                if 0 < len(parts):
                    for line_y in reversed(self.space.check_completed_parts()):
                        self.space.delete_part(line_y)

                    self._listener_manager.call_event(PartDeleteEvent(len(parts)))

        else:
            self.active_tetromino = moved_tetromino

            next_tetromino = self.active_tetromino.moved(0, -1, 0)
            if self.space.is_collision(next_tetromino):
                self._listener_manager.call_event(
                    TetrominoDownCollisionEvent(CollisionReason.TICK)
                )
