from tetris_generic import Cell
from tetris_generic import Space
from tetris_generic.tetromino import Tetromino
from .const import DEFAULT_SPACE_HEIGHT
from .const import DEFAULT_SPACE_WIDTH


class DefaultSpace(Space):
    def __init__(
            self,
            width: int = DEFAULT_SPACE_WIDTH,
            height: int = DEFAULT_SPACE_HEIGHT
    ):
        self.width: int = width
        self.height: int = height
        self.data: list[list[Cell | None]] = [
            [None for x in range(self.width)]
            for y in range(self.height)
        ]

    def is_filled(self, x: int, y: int, outside_auto_fill: bool = True) -> bool:
        if x < 0 or y < 0:
            if outside_auto_fill:
                return True
            else:
                raise IndexError(f'Position {x}, {y} is outside of space')

        try:
            return self.data[y][x] is not None
        except IndexError:
            if outside_auto_fill:
                return True
            else:
                raise IndexError(f'Position {x}, {y} is outside of space')

    def __getitem__(self, position: tuple[int, int]) -> Cell | None:
        x, y = position
        return self.data[y][x]
    def __setitem__(self, position: tuple[int, int], cell: Cell | None):
        x, y = position
        self.data[y][x] = cell

    def is_collision(self, tetromino: Tetromino) -> bool:
        for dy in range(tetromino.type.size):
            for dx in range(tetromino.type.size):
                x, y = tetromino.x + dx, tetromino.y + dy
                if self.is_filled(x, y) and tetromino[dx, dy]:
                    return True

        return False

    def get_dropped(self, input_tetromino: Tetromino) -> Tetromino:
        tetromino = input_tetromino

        while True:
            moved_tetromino = tetromino.moved(0, -1, 0)
            if self.is_collision(moved_tetromino):
                return tetromino
            else:
                tetromino = moved_tetromino

    def check_completed_parts(self) -> list[int]:
        filled_lines = list()

        for y in range(self.height):
            is_filled = True
            for x in range(self.width):
                if not self.is_filled(x, y):
                    is_filled = False

            if is_filled:
                filled_lines.append(y)

        return filled_lines

    def delete_part(self, part_position: int):
        for y in range(part_position, self.height):
            for x in range(self.width):
                try:
                    cell = self[x, y + 1]
                except IndexError:
                    cell = None

                self[x, y] = cell