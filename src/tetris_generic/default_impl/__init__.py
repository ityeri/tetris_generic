from tetris_generic import TetrisGame
from .const import DEFAULT_SPACE_WIDTH, DEFAULT_SPACE_HEIGHT
from .default_space import DefaultSpace
from . import tetrominos
from .default_tetromino_spawner import DefaultTetrominoSpawner
from .colour_cell import ColourCell


def create_default_game() -> TetrisGame:
    space = DefaultSpace()
    spawner = DefaultTetrominoSpawner()

    return TetrisGame(
        initial_space=space,
        spawner=spawner
    )

__all__ = [
    'DEFAULT_SPACE_WIDTH',
    'DEFAULT_SPACE_HEIGHT',
    'create_default_game',

    'DefaultSpace',
    'tetrominos',
    'DefaultTetrominoSpawner',
    'ColourCell'
]