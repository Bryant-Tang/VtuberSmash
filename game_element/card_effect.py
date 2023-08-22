from abc import abstractmethod
from typing import Any
from game_logic import CardEffect as LogicCardEffect
from gui_components import Component, Surface

from .creating_information import CardEffectCreatingInformation


class CardEffect(LogicCardEffect, Component):
    name: str

    def __init__(self, affect_target: str, affect_attribute: str, affect_operation: str, affect_timing: str, affect_value: Any, affect_probability: float,
                 background: Surface, name: str) -> None:
        LogicCardEffect.__init__(self, affect_target, affect_attribute, affect_operation,
                                 affect_timing, affect_value, affect_probability)
        Component.__init__(self, background)
        self.name = name

    def copy(self):
        return CardEffect(self.affect_target, self.affect_attribute, self.affect_operation, self.affect_timing, self.affect_probability,
                          self.get_background(), self.name)

    def get_creating_information(self):
        return CardEffectCreatingInformation(self.name, self.affect_value, self.affect_probability)
