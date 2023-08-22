from typing import List
from gui_components import Frame, Component
import source
import pygame
import random

from .decorator import singleton
from .player import Player
from .card import Card
from . import player_factory


@singleton
class GameFrame(Frame):
    _player: Player
    _enemy: Player
    _game_running: bool
    _all_card_list: List[Card]
    _all_player_detail_list: List[Component]

    def __init__(self) -> None:
        bgm_list = [source.audio.get_sound(source.audio.BGM_000),
                    source.audio.get_sound(source.audio.BGM_001),
                    source.audio.get_sound(source.audio.BGM_002),
                    source.audio.get_sound(source.audio.BGM_003)]
        random.shuffle(bgm_list)
        super().__init__((source.constants.WINDOW_WIDTH,
                          source.constants.WINDOW_HEIGHT), bgm_list)
        pygame.display.set_caption(source.constants.GAME_TITLE)
        self._player = None
        self._enemy = None
        self._all_card_list = []
        self._game_running = None
        self._all_player_detail_list = [
            Component(source.image.player_detail(i)) for i in range(player_factory.get_all_player_count())]

    def get_all_player_detail(self):
        return self._all_player_detail_list

    def add_card(self, card: Card) -> None:
        self._all_card_list.append(card)

    def get_all_card(self) -> List[Card]:
        return [card.copy() for card in self._all_card_list]

    def set_player(self, player: Player) -> None:
        self._player = player

    def set_enemy(self, enemy: Player) -> None:
        self._enemy = enemy

    def get_player(self) -> Player:
        return self._player.copy()

    def get_enemy(self) -> Player:
        return self._enemy.copy()

    def is_game_running(self) -> bool:
        if self._game_running:
            return True
        return False

    def gui_loop(self) -> None:
        
        self._game_running = True
        while self._game_running:
            GameFrame().handle_input()
            GameFrame().paint()