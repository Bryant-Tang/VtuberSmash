from typing import Tuple
from game_resource import Color, constants, font

from .box import Box


class Label(Box):
    _text: str
    _color: Color
    _text_size: int

    def __init__(self, text: str = "", color: Color = constants.DEFAULT_FONT_COLOR, text_size: int = constants.DEFAULT_FONT_SIZE) -> None:
        self._font_name = font.DEFAULT
        super().__init__(font.get_font(
            self._font_name, text_size).render(text, True, color))
        self._text = text
        self._color = Color(color)
        self._text_size = text_size
        self._surface = font.get_font(self._font_name, self._text_size).render(self._text, True, self._color)
        self.auto_set_size()

    def set_text(self, text: str) -> None:
        self._text = text
        self._surface = font.get_font(self._font_name, self._text_size).render(
            self._text, True, self._color)
        self.auto_set_size()

    def set_color(self, color: Color) -> None:
        self._color = Color(color)
        self._surface = font.get_font(self._font_name, self._text_size).render(
            self._text, True, self._color)
        self.auto_set_size()

    def set_text_size(self, text_size: int) -> None:
        self._text_size = text_size
        self._surface = font.get_font(self._font_name, self._text_size).render(
            self._text, True, self._color)
        self.auto_set_size()

    def set_size(self, size: Tuple[int, int]) -> None:
        self.auto_set_size()

    def auto_set_size(self) -> None:
        self._collision_rect.size = self._surface.get_rect().size

    def get_text(self) -> str:
        return self._text

    def get_color(self) -> Color:
        return Color(self._color)

    def get_text_size(self) -> int:
        return self._text_size