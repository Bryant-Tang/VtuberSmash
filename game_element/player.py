from typing import List
from game_logic import Player as LogicPlayer, Card as LogicCard, PlayerEffect
from gui_components import Surface, Player as GuiPlayer


class Player(LogicPlayer, GuiPlayer):
    name: str
    _id: int

    def __init__(self, player_id: int, name: str, background: Surface, hp: int, shield: int, max_hp: int, max_shield: int, player_effect_list: List[PlayerEffect] = [], deck: List[LogicCard] = []) -> None:
        LogicPlayer.__init__(self, hp, shield, max_hp, max_shield,
                             player_effect_list, deck)
        GuiPlayer.__init__(self, background, hp, shield, max_hp, max_shield)
        self._id = player_id
        self.name = name

    def get_player_id(self):
        return self._id
