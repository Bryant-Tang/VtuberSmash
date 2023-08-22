import threading
from typing import List
from typing_extensions import Self

from gui_components import ValueBar, Box
from pygame import Surface, Rect
import source
import pygame

from .deck import Deck
from .player_effect import EffectTarget, PlayerEffect
from .player_attribute import Attribute


class Player(Box, EffectTarget):
    _hp: ValueBar
    _max_hp: int
    _shield: ValueBar
    _max_shield: int
    _is_invert: bool
    _name: str
    _value_bar_spacing: int
    _deck: Deck
    _id: int
    _effect_list: List[int]

    def __init__(self, background: Surface, id: int, hp: int, shield: int, max_hp: int, max_shield: int, deck: Deck, rect: Rect = None, name: str = "unknown", value_bar_spacing: int = 5) -> None:
        super().__init__(background, rect)
        self._is_invert = False
        self._value_bar_spacing = value_bar_spacing
        self._id = id
        self.set_deck(deck)
        self._effect_list = []

        self._max_hp = max_hp
        self._hp = ValueBar(source.image.get_image(source.image.PLAYER_HP),
                            source.image.get_image(source.image.PLAYER_HP_BG),
                            initial_value=hp, max_value=self._max_hp, spacing=-20)
        self.add_component(self._hp)

        self._max_shield = max_shield
        self._shield = ValueBar(source.image.get_image(source.image.PLAYER_SHIELD),
                                source.image.get_image(
                                    source.image.PLAYER_SHIELD_BG),
                                initial_value=shield, max_value=self._max_shield, spacing=-20)
        self.add_component(self._shield)

        self._set_value_bar_pos()
        self.set_name(name)

    def set_deck(self, deck: Deck) -> None:
        self._deck = deck

    def get_id(self) -> int:
        return self._id

    def set_name(self, name: str) -> None:
        self._name = name

    def get_name(self) -> str:
        return self._name

    def set_rotate(self, is_invert: bool):
        if self._is_invert != is_invert:
            self.set_background(pygame.transform.rotate(self._surface, 180))
        self._is_invert = is_invert
        self._set_value_bar_pos()

    def _set_value_bar_pos(self):
        if self._is_invert:
            self._hp.set_center((self.get_width()//2,
                                 self._hp.get_height()//2))
            self._shield.set_center((self.get_width()//2,
                                     self._hp.get_height() + self._shield.get_height()//2 + self._value_bar_spacing))
        else:
            self._hp.set_center((self.get_width()//2,
                                 self.get_height() - self._hp.get_height()//2))
            self._shield.set_center((self.get_width()//2,
                                     self._hp.get_y() - self._shield.get_height()//2 - self._value_bar_spacing))

    def add_effect(self, effect: int) -> None:
        self._effect_list.append(effect)

    def remove_effect(self, effect: int) -> None:
        if effect in self._effect_list:
            self._effect_list.remove(effect)

    def get_effect(self):
        return self._effect_list.copy()

    # def is_contain_effect(self, timing: str):
    #     for effect in self._effect_list:
    #         if effect.is_contain_timing(timing):
    #             return True
    #     return False

    # def check_effect(self):
    #     for effect in self._effect_list:
    #         if effect.is_fail():
    #             self.remove_effect(effect)

    # def do_effect(self, attribute: str, value: int,  timing: str):
    #     for effect in self._effect_list:
    #         attribute, value = effect.do_effect(self, attribute, value, timing)
    #     return attribute, value

    # def do_effect_with_delay(self, attribute: str, value: int,  timing: str):
    #     pygame.time.delay(1000)
    #     self.do_effect(attribute, value,  timing)

    # def modify_attributes(self,  attribute: str, value: int):
    #     attribute, value = self.do_effect(attribute, value,
    #                                       PlayerEffect.BEFORE_MODIFY_VALUE)
    #     if attribute == Attribute.HP:
    #         self.add_hp(value)
    #     elif attribute == Attribute.SHIELD:
    #         self.add_shield(value)
    #     threading.Thread(target=self.do_effect_with_delay, args=[
    #                      attribute, value, PlayerEffect.AFTER_MODIFY_VALUE]).start()

    def add_hp(self, value: int):
        if self._hp.get_value() + value > self._max_hp:
            self._hp.add_value(self._max_hp - self._hp.get_value())
        else:
            self._hp.add_value(value)

    def get_hp_value(self) -> int:
        return self._hp.get_value()

    def add_shield(self, value: int):
        shield_end_value = self._shield.get_value() + value
        if shield_end_value > self._max_shield:
            self._shield.add_value(self._max_shield - self._shield.get_value())
        elif shield_end_value >= 0:
            self._shield.add_value(value)
        else:
            self._shield.add_value(value - shield_end_value)
            self.add_hp(shield_end_value)

    def get_shield_value(self) -> int:
        return self._shield.get_value()

    def draw_card(self, num: int):
        return self._deck.draw_card(num)

    def get_deck(self) -> Deck:
        return self._deck.copy()

    def copy(self) -> Self:
        player = Player(self._surface, self.get_id(), self.get_hp_value(), self.get_shield_value(
        ), self._max_hp, self._max_shield, self._deck.copy(), name=self._name, value_bar_spacing=self._value_bar_spacing)
        for effect in self._effect_list:
            player.add_effect(effect)
        return player
