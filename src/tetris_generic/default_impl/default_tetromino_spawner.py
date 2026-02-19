from random import choice

from math import floor, ceil

from tetris_generic.tetromino import Tetromino, TetrominoType
from tetris_generic.tetromino.tetromino_spawner import TetrominoSpawner
from .const import DEFAULT_SPACE_WIDTH, DEFAULT_SPACE_HEIGHT
from .tetrominos import tetromino_types


# TODO separate this into Spawner, TypeSelector
class DefaultTetrominoSpawner(TetrominoSpawner):
    def __init__(
            self,
            space_width: int = DEFAULT_SPACE_WIDTH,
            space_height: int = DEFAULT_SPACE_HEIGHT,
            que_length: int = 5
    ):
        self.space_width: int = space_width
        self.space_height: int = space_height
        self.selected_tetromino_types: list[TetrominoType] = list()
        self.que_length: int = que_length
        self.tetromino_que: list[TetrominoType] = [self.next_tetromino_type() for _ in range(que_length)]

    def next_tetromino_type(self) -> TetrominoType:
        if len(self.selected_tetromino_types) == 7:
            self.selected_tetromino_types.clear()

        remine_types = [
            tetromino_type for tetromino_type in tetromino_types
            if tetromino_type not in self.selected_tetromino_types
        ]

        next_type = choice(remine_types)
        self.selected_tetromino_types.append(next_type)

        return next_type

    def next(self) -> Tetromino:
        self.tetromino_que.append(self.next_tetromino_type())
        selected_type = self.tetromino_que.pop(0)

        center_x = floor(self.space_width / 2)

        if self.space_width % 2 == 0:
            x = center_x - ceil(selected_type.size / 2)
        else:
            x = center_x - floor(selected_type.size / 2)

        if selected_type.size == 4:
            y = self.space_height - 3
        elif selected_type.size == 3:
            y = self.space_height - 3
        elif selected_type.size == 2:
            y = self.space_height - 2
        else:
            raise ValueError('Invalid tetromino type')

        return Tetromino(
            x=x,
            y=y,
            rotation=0,
            type=selected_type
        )