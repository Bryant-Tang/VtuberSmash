from abc import abstractmethod
from game_logic import PlayerEffect as LogicPlayerEffect
from gui_components import Component, Surface

from .creating_information import PlayerEffectCreatingInformation


class PlayerEffect(LogicPlayerEffect, Component):
    name: str
    background_name: str

    def __init__(self, affect_timing: str, max_affect_times: int, max_affect_round: int,
                 background: Surface, background_name: str, name: str) -> None:
        LogicPlayerEffect.__init__(self,
                                   affect_timing, max_affect_times, max_affect_round)
        Component.__init__(self, background)
        self.background_name = background_name
        self.name = name

    def copy(self):
        return PlayerEffect(self.affect_timing, self.max_affect_times, self.max_affect_round,
                            self.get_background(), self.name)

    def get_creating_information(self) -> PlayerEffectCreatingInformation:
        return PlayerEffectCreatingInformation(self.name, self.max_affect_times, self.max_affect_round)
