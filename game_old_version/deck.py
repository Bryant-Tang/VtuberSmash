import random
from typing import List
from typing_extensions import Self

from .card import Card


class Deck:
    _card_list: List[Card]

    def __init__(self, card_list: List[Card]) -> None:
        self._card_list = []
        self._card_list.extend(card_list)

    def draw_card(self, num: int) -> List[Card]:
        drawn_card_list = []
        for _ in range(num):
            if len(self._card_list) == 0:
                break
            drawn_card = random.choice(self._card_list)
            drawn_card_list.append(drawn_card)
            self._card_list.remove(drawn_card)
        return drawn_card_list

    def get_all_card(self) -> List[Card]:
        return [card.copy() for card in self._card_list]

    def copy(self) -> Self:
        return Deck([card.copy() for card in self._card_list])
