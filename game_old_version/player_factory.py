from typing import List
import source

from .player import Player
from .deck import Deck
from .card import Card

_player_attribute = {0: {"hp": 23, "shield": 10, "max_hp": 45, "max_shield": 10},
                     1: {"hp": 20, "shield": 15, "max_hp": 40, "max_shield": 20},
                     2: {"hp": 20, "shield": 15, "max_hp": 35, "max_shield": 30},
                     3: {"hp": 20, "shield": 15, "max_hp": 30, "max_shield": 40},
                     4: {"hp": 20, "shield": 15, "max_hp": 25, "max_shield": 50},
                     5: {"hp": 20, "shield": 15, "max_hp": 20, "max_shield": 60}, }


def get_all_player_count():
    return len(_player_attribute)


def get_player(id: int, name: str, card_list: List[Card]) -> Player:
    return Player(source.image.player(id), id, hp=_player_attribute[id]["hp"], shield=_player_attribute[id]["shield"],
                  max_hp=_player_attribute[id]["max_hp"], max_shield=_player_attribute[id]["max_shield"], deck=Deck(card_list), name=name)
