from abc import ABC, abstractmethod


class Cell(ABC):
    @abstractmethod
    def get_display_color(self) -> tuple[int, int, int]: ...
