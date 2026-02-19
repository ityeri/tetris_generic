from tetris_generic import Cell


class ColourCell(Cell):
    def __init__(self, color: tuple[int, int, int]):
        self.color: tuple[int, int, int] = color

    def get_display_color(self) -> tuple[int, int, int]:
        return self.color
