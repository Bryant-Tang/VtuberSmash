from typing import List
from gui_components import Card as GuiCard, Surface
from game_logic import Card as LogicCard
from pygame.mixer import Sound
from .card_effect import CardEffect


class Card(LogicCard, GuiCard):
    _id: int
    _sound: Sound

    def __init__(self, card_id: int, background: Surface, effect_list: List[CardEffect], attack_sound: Sound) -> None:
        LogicCard.__init__(self, effect_list)
        GuiCard.__init__(self, background)
        self._id = card_id
        self._sound = attack_sound

    def get_card_id(self):
        return self._id

    def play_attack_sound(self):
        self._sound.play()
