from prompt_toolkit.formatted_text import OneStyleAndTextTuple, StyleAndTextTuples


class FormattedTextSurface:
    def __init__(
            self,
            width: int,
            height: int,
            pixel_width: int,
            pixel_height: int,
            initial_character: OneStyleAndTextTuple = ('', ' ')
    ):
        self.width: int = width
        self.height: int = height
        self.pixel_width: int = pixel_width
        self.pixel_height: int = pixel_height
        self._data: list[list[OneStyleAndTextTuple]] = [[initial_character for x in range(width)] for y in range(height)]

    def __getitem__(self, position: tuple[int, int]) -> OneStyleAndTextTuple:
        x, y = position
        return self._data[y][x]
    def __setitem__(self, position: tuple[int, int], value: OneStyleAndTextTuple):
        x, y = position
        self._data[y][x] = value

    @property
    def h_characters(self):
        return self.width * self.pixel_width
    @property
    def v_characters(self):
        return self.height * self.pixel_height

    def fill(self, text: OneStyleAndTextTuple):
        for y in range(self.height):
            for x in range(self.width):
                self[x, y] = text

    def render(self) -> StyleAndTextTuples:
        extended_data = [
            [
                text
                for text in line
                for sub_x in range(self.pixel_width)
            ]
            for line in self._data
            for sub_y in range(self.pixel_height)
        ]

        return [
            text
            for line in extended_data
            for text in line + [('', '\n')]
        ]