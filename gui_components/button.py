from typing import Union
from game_resource import audio, constants, image

from .component import pygame_mouse
from .box import Box, Surface
from .label import Label
from .mouse_event_handler import MouseEventAdapter


class BaseButton(Box):
    _down_surface: Surface
    _up_surface: Surface

    def __init__(self, up_background: Surface, down_background: Surface) -> None:
        super().__init__(up_background)
        self._up_surface = up_background
        self._down_surface = down_background
        self.add_mouse_handler(MouseEventAdapter(mouse_down=lambda event: self._change_bg_to_down(),
                                                 mouse_up=lambda event: self._change_bg_to_up(),
                                                 any_event=self._handle_any_event))
        self.add_mouse_handler(MouseEventAdapter(mouse_click=lambda event: audio.get_sound(audio.EFFECT_BTN_UP).play(),
                                                 mouse_down=lambda event: audio.get_sound(audio.EFFECT_BTN_DOWN).play()))

    def _handle_any_event(self, event):
        mouse_pos = pygame_mouse.get_pos()
        if not self.is_collide(mouse_pos):
            self._change_bg_to_up()

    def _change_bg_to_up(self) -> None:
        self.set_background(self._up_surface)

    def _change_bg_to_down(self) -> None:
        self.set_background(self._down_surface)

    def set_background_pair(self, background_up: Surface, background_down: Surface) -> None:
        self._up_surface = background_up
        self._down_surface = background_down
        return super().set_background(background_up)


class TextButton(BaseButton):
    _text_size: int

    def __init__(self, text: str = None, text_size: int = constants.DEFAULT_FONT_SIZE) -> None:
        super().__init__(image.get_image(image.BTN_TEXT_UP),
                         image.get_image(image.BTN_TEXT_DOWN))
        self.set_size((constants.DEFAULT_TEXT_BTN_WIDTH,
                      constants.DEFAULT_TEXT_BTN_HEIGHT))
        self._text_size = text_size
        if text:
            self.add_text(text)

    def set_width(self, width: int) -> None:
        super_result = super().set_width(width)
        for comp in self.get_components():
            comp.set_center((self.get_width()//2, self.get_height()//2))
        return super_result

    def set_height(self, height: int) -> None:
        super_result = super().set_height(height)
        for comp in self.get_components():
            comp.set_center((self.get_width()//2, self.get_height()//2))
        return super_result

    def add_text(self, text: str) -> None:
        text_comp = Label(text, constants.COLOR_WHITE, self._text_size)
        text_comp.set_center((self.get_width()//2, self.get_height()//2))
        self.add_component(text_comp)

    def remove_text(self, text: str) -> None:
        for comp in self._children:
            if comp is Label and comp.get_text() == text:
                self.remove_component(comp)
                break


class RoundButton(BaseButton):
    def __init__(self, up_background: Surface, down_background: Surface) -> None:
        super().__init__(up_background, down_background)
        self.set_size((constants.DEFAULT_ROUND_BTN_WIDTH,
                      constants.DEFAULT_ROUND_BTN_HEIGHT))
