from abc import ABC
from dataclasses import dataclass
from enum import Enum, auto

from tetris_generic.tetromino import Tetromino


class TetrisEvent(ABC): ...


class CollisionReason(Enum):
    CONTROL = auto()
    TICK = auto()

@dataclass
class TetrominoDownCollisionEvent(TetrisEvent):
    reason: CollisionReason

@dataclass
class TetrominoDropEvent(TetrisEvent):
    ...

@dataclass
class TetrominoLandingEvent(TetrisEvent):
    before_tetromino: Tetromino | None
    after_tetromino: Tetromino | None

@dataclass
class PartDeleteEvent(TetrisEvent):
    deleted_parts: int

@dataclass
class GameOverEvent(TetrisEvent):
    ...