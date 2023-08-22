from typing_extensions import Self
from gui_components import Box
from pygame import Surface, Rect


class Card(Box):
    _id: int
    _effect_id: int

    def __init__(self, background: Surface, id: int, effect_id: int, rect: Rect = None) -> None:
        super().__init__(background, rect)
        self._id = id
        self._effect_id = effect_id

    def get_id(self) -> int:
        return self._id

    def get_effect_id(self) -> int:
        return self._effect_id

    def copy(self) -> Self:
        card = Card(self._surface, self._id, self._effect_id)
        card.set_size(self.get_size())
        return card
