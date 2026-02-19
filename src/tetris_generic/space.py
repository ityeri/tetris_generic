from abc import ABC, abstractmethod

from tetris_generic.cell import Cell
from tetris_generic.tetromino import Tetromino


class Space(ABC):
    @abstractmethod
    def is_filled(self, x: int, y: int) -> bool: ...

    @abstractmethod
    def __getitem__(self, position: tuple[int, int]) -> Cell | None: ...

    @abstractmethod
    def __setitem__(self, position: tuple[int, int], cell: Cell | None): ...

    @abstractmethod
    def is_collision(self, tetromino: Tetromino) -> bool: ...

    @abstractmethod
    def get_dropped(self, tetromino: Tetromino) -> Tetromino: ...

    @abstractmethod
    def check_completed_parts(self) -> list[int]: ...

    @abstractmethod
    def delete_part(self, part_position: int): ...