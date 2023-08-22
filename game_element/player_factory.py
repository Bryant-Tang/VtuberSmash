from typing import Dict, List, Tuple, Union
from .player import Player
from game_resource import image
from gui_components import Component

from .creating_information import PlayerCreatingInformation
from .effect_factory import get_player_effect
from .card_factory import get_card

_default_player_attribute: Dict[int, PlayerCreatingInformation]


def init():
    global _default_player_attribute
    _default_player_attribute = {
        0: PlayerCreatingInformation(0, "涅默", 15, 10, 45, 10, [], []),
        1: PlayerCreatingInformation(1, "厄倫蒂兒", 15, 10, 40, 20, [], []),
        2: PlayerCreatingInformation(2, "埃穆亞", 15, 10, 35, 30, [], []),
        3: PlayerCreatingInformation(3, "熙歌", 15, 10, 30, 40, [], []),
        4: PlayerCreatingInformation(4, "KSP", 15, 10, 25, 50, [], []),
        5: PlayerCreatingInformation(5, "汐", 15, 10, 20, 60, [], []),
    }


def get_player(player_creating_information_or_name: PlayerCreatingInformation):
    return Player(player_creating_information_or_name.player_id,
                  player_creating_information_or_name.name,
                  image.player(
                      player_creating_information_or_name.player_id),
                  player_creating_information_or_name.hp,
                  player_creating_information_or_name.shield,
                  player_creating_information_or_name.max_hp,
                  player_creating_information_or_name.max_shield,
                  [get_player_effect(
                      effect) for effect in player_creating_information_or_name.effect_list],
                  [get_card(card_id) for card_id in player_creating_information_or_name.deck])


def get_default_player_creating_information(player_id: int):
    return _default_player_attribute[player_id]


def get_player_detail(player_id: int):
    return Component(image.player_detail(player_id))


def get_player_fullbody_comp(player_id: int):
    return Component(image.player_fullbody(player_id))


def get_all_player_id():
    return [player_id for player_id in _default_player_attribute.keys()]
