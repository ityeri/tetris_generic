from abc import ABC, abstractmethod

from .tetromino import Tetromino


class TetrominoSpawner(ABC):
    @abstractmethod
    def next(self) -> Tetromino: ...