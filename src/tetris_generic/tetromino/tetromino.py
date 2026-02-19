from dataclasses import dataclass

from tetris_generic.cell import Cell

RawWallKickData = dict[tuple[int, int], list[tuple[int, int]]]

@dataclass
class WallKickData:
    data: RawWallKickData

    def get(self, before: int, after: int) -> list[tuple[int, int]]:
        return self.data[(before % 4, after % 4)]

@dataclass
class TetrominoType:
    size: int
    data: list[list[bool]]
    wall_kick_data: WallKickData
    filling_cell: Cell

def shape_from_string(size, *shape_lines: str) -> list[list[bool]]:
    data = [[c != ' ' for c in line] for line in reversed(shape_lines)]

    if len(data) != size:
        raise ValueError(f'Passed size and actual shape is unmatched')

    for line in data:
        if len(line) != size:
            raise ValueError(f'Passed size and actual shape is unmatched')

    return data

@dataclass(frozen=True)
class Tetromino:
    x: int
    y: int
    rotation: int
    type: TetrominoType

    def moved(self, x_offset: int, y_offset: int, rotate: int):
        return Tetromino(
            x=self.x + x_offset,
            y=self.y + y_offset,
            rotation=(self.rotation + rotate) % 4,
            type=self.type
        )

    def __getitem__(self, position: tuple[int, int]) -> bool:
        x, y = position

        if self.rotation == 0:
            dx, dy = x, y
        elif self.rotation == 1:
            dx, dy = self.type.size - y - 1, x
        elif self.rotation == 2:
            dx, dy = self.type.size - x - 1, self.type.size - y - 1
        elif self.rotation == 3:
            dx, dy = y, self.type.size - x - 1
        else:
            raise ValueError(f'Invalid rotation value: {self.rotation}')

        return self.type.data[dy][dx]
