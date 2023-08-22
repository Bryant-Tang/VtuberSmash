from .box import Box, Surface
from .value_bar import ValueBar
from game_resource import image
from pygame import transform as pygame_transform


class Player(Box):
    _hp_bar: ValueBar
    _shield_bar: ValueBar
    _max_hp_bar: ValueBar
    _max_shield_bar: ValueBar
    _is_invert: bool
    _value_bar_spacing: int

    def __init__(self, background: Surface, initial_hp: int, initial_shield: int, max_hp: int, max_shield: int, value_bar_spacing: int = 5) -> None:
        super().__init__(background)
        self._is_invert = False
        self._value_bar_spacing = value_bar_spacing
        self._max_hp_bar = ValueBar(image.get_image(image.PLAYER_HP_BG),
                                    initial_value=max_hp, spacing=-20)
        self.add_component(self._max_hp_bar)
        self._max_shield_bar = ValueBar(image.get_image(image.PLAYER_SHIELD_BG),
                                        initial_value=max_shield, spacing=-20)
        self.add_component(self._max_shield_bar)
        self._hp_bar = ValueBar(image.get_image(image.PLAYER_HP),
                                initial_value=initial_hp,  spacing=-20)
        self.add_component(self._hp_bar)
        self._shield_bar = ValueBar(image.get_image(image.PLAYER_SHIELD),
                                    initial_value=initial_shield, spacing=-20)
        self.add_component(self._shield_bar)
        self._set_value_bar_pos()

    def set_invert(self, is_invert: bool):
        if self._is_invert != is_invert:
            self.set_background(pygame_transform.rotate(self._surface, 180))
        self._is_invert = is_invert
        self._set_value_bar_pos()

    def _set_value_bar_pos(self):
        if self._is_invert:
            self._max_hp_bar.set_y(0)
            self._max_hp_bar.set_x(
                self.get_width()//2 - max(self._max_hp_bar.get_width(), self._max_shield_bar.get_width())//2)
            self._hp_bar.set_pos(self._max_hp_bar.get_pos())
            self._max_shield_bar.set_pos((self._max_hp_bar.get_x(),
                                          self._max_hp_bar.get_bottom() + self._value_bar_spacing))
            self._shield_bar.set_pos(self._max_shield_bar.get_pos())
        else:
            self._max_hp_bar.set_y(self.get_height() -
                                   self._max_hp_bar.get_height())
            self._max_hp_bar.set_x(
                self.get_width()//2 - max(self._max_hp_bar.get_width(), self._max_shield_bar.get_width())//2)
            self._hp_bar.set_pos(self._max_hp_bar.get_pos())
            self._max_shield_bar.set_pos((self._max_hp_bar.get_x(),
                                          self._max_hp_bar.get_top() - self._max_shield_bar.get_height() - self._value_bar_spacing))
            self._shield_bar.set_pos(self._max_shield_bar.get_pos())

    def set_max_hp_bar_value(self, value: int):
        self._max_hp_bar.set_value(value)

    def set_hp_bar_value(self, value: int):
        self._hp_bar.set_value(value)

    def set_max_shield_bar_value(self, value: int):
        self._max_shield_bar.set_value(value)

    def set_shield_bar_value(self, value: int):
        self._shield_bar.set_value(value)
