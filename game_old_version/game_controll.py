from gui_components import Component
import threading
from typing import List
import pygame
import source

from .battle_scene import ChooseCardScene, FightScene
from .menu_scene import MenuScene
from .rule_scene import RuleScene
from .card_edit_scene import CardEditScene
from .player_edit_scene import PlayerEditScene
from .game_frame import GameFrame
from .card import Card
from .deck import Deck
from .player_effect import EffectTarget
from . import card_factory, card_effect, player_factory, player_effect, battle_scene, card_edit_scene, player_edit_scene


def init():
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    pygame.display.set_icon(source.image.get_image(source.image.ICON))
    init_game_frame()
    init_menu_scene()
    init_rule_scene()
    init_card_edit_scene()
    init_player_edit_scene()
    init_battle_scene()
    init_choose_card_scene()
    init_fight_scene()
    init_card_effect()
    init_player_effect()


def init_game_frame():
    card_list = []
    for _ in range(2):
        for i in range(8):
            card_list.append(card_factory.get_card(i))
    # player = player_factory.get_player(0, "player", [card_factory.get_card(997),card_factory.get_card(997),card_factory.get_card(997),card_factory.get_card(997)])
    # enemy = player_factory.get_player(4, "enemy", [card_factory.get_card(7),card_factory.get_card(7),card_factory.get_card(7),card_factory.get_card(7)])
    player = player_factory.get_player(0, "player", card_list)
    enemy = player_factory.get_player(4, "enemy", card_list)
    GameFrame().set_player(player)
    GameFrame().set_enemy(enemy)
    for i in range(12):
        GameFrame().add_card(card_factory.get_card(i))
    for i in range(600, 605):
        GameFrame().add_card(card_factory.get_card(i))


def init_card_effect():
    def get_player_attack_card_list():
        return FightScene().get_player_attack_card_list()

    def get_player_remain_card_list():
        return FightScene().get_player_remain_card_list()

    def get_enemy_card_list():
        return FightScene().get_enemy_attack_card_list()

    def get_enemy_remain_card_list():
        return FightScene().get_enemy_remain_card_list()

    def get_player():
        return FightScene().get_player()

    def get_enemy():
        return FightScene().get_enemy()

    def get_current_round():
        return FightScene().get_current_round()
    card_effect.init(get_player_card_list=get_player_attack_card_list,
                     get_player_remain_card_list=get_player_remain_card_list,
                     get_enemy_card_list=get_enemy_card_list,
                     get_enemy_remain_card_list=get_enemy_remain_card_list,
                     get_player=get_player,
                     get_enemy=get_enemy,
                     get_current_round=get_current_round)


def init_player_effect():
    def add_effect_icon(icon: Component):
        icon = FightScene().add_effect_icon(icon)
        pygame.time.delay(2000)
        FightScene().remove_effect_icon(icon)

    def get_player_card_list(player: EffectTarget):
        if FightScene().get_player() is player:
            return FightScene().get_player_attack_card_list()
        elif FightScene().get_enemy() is player:
            return FightScene().get_enemy_attack_card_list()
        return []

    def get_player_remain_card_list(player: EffectTarget):
        if FightScene().get_player() is player:
            return FightScene().get_player_remain_card_list()
        elif FightScene().get_enemy() is player:
            return FightScene().get_enemy_remain_card_list()
        return []

    def get_enemy_card_list(player: EffectTarget):
        if FightScene().get_player() is player:
            return FightScene().get_enemy_attack_card_list()
        elif FightScene().get_enemy() is player:
            return FightScene().get_player_attack_card_list()
        return []

    def get_enemy_remain_card_list(player: EffectTarget):
        if FightScene().get_player() is player:
            return FightScene().get_enemy_remain_card_list()
        elif FightScene().get_enemy() is player:
            return FightScene().get_player_remain_card_list()
        return []

    def get_enemy(player: EffectTarget):
        if FightScene().get_player() is player:
            return FightScene().get_enemy()
        elif FightScene().get_enemy() is player:
            return FightScene().get_player()
        return []

    def get_current_round():
        return FightScene().get_current_round()
    player_effect.init(add_effect_icon=add_effect_icon,
                       get_player_card_list=get_player_card_list, get_player_remain_card_list=get_player_remain_card_list,
                       get_enemy_card_list=get_enemy_card_list, get_enemy_remain_card_list=get_enemy_remain_card_list,
                       get_enemy=get_enemy, get_current_round=get_current_round)


def init_menu_scene():
    def start_battle():
        GameFrame().set_scene(ChooseCardScene())

        def start_battle():
            ChooseCardScene().start(True)
        threading.Thread(target=start_battle).start()

    def read_rule():
        GameFrame().set_scene(RuleScene())

    def edit_card():
        GameFrame().set_scene(CardEditScene())

        def show_card():
            CardEditScene().show_card()
        threading.Thread(target=show_card).start()

    def edit_player():
        GameFrame().set_scene(PlayerEditScene())

        def show_player():
            PlayerEditScene().show_player()
        threading.Thread(target=show_player).start()
    MenuScene().init(start_battle=start_battle, read_rule=read_rule,
                     edit_card=edit_card, edit_player=edit_player)


def init_rule_scene():
    def back_to_menu():
        GameFrame().set_scene(MenuScene())
    RuleScene().init(back_to_menu=back_to_menu)


def init_card_edit_scene():
    def back_to_menu_with_setting_card_list(card_list: List[Card]):
        GameFrame().set_scene(MenuScene())
        player = GameFrame().get_player()
        player.set_deck(Deck(card_list))
        GameFrame().set_player(player)

    def get_all_card():
        return GameFrame().get_all_card()

    def get_selected_card():
        return GameFrame().get_player().get_deck().get_all_card()
    card_edit_scene.init(get_all_card=get_all_card,
                         get_selected_card=get_selected_card)
    CardEditScene().init(
        back_to_menu_with_setting_card_list=back_to_menu_with_setting_card_list)


def init_player_edit_scene():
    def back_to_menu_with_setting_player(player_id: int):
        GameFrame().set_scene(MenuScene())
        card_list = GameFrame().get_player().get_deck().get_all_card()
        GameFrame().set_player(player_factory.get_player(player_id, "player", card_list))

    def get_all_player():
        return GameFrame().get_all_player_detail()

    def get_current_player():
        return GameFrame().get_player()
    player_edit_scene.init(get_all_player=get_all_player,
                           get_current_player=get_current_player)
    PlayerEditScene().init(back_to_menu_with_setting_player=back_to_menu_with_setting_player)


def init_battle_scene():
    def get_player():
        return GameFrame().get_player()

    def get_enemy():
        return GameFrame().get_enemy()
    battle_scene.init(get_player=get_player, get_enemy=get_enemy)


def init_choose_card_scene():
    def go_to_fight_scene():
        GameFrame().set_scene(FightScene())

        def fight():
            FightScene().fight()
        threading.Thread(target=fight).start()
    ChooseCardScene().init(go_to_fight_scene=go_to_fight_scene)


def init_fight_scene():
    def go_next_round():
        GameFrame().set_scene(ChooseCardScene())

        def start_next_round():
            ChooseCardScene().start(False)
        threading.Thread(target=start_next_round).start()

    def back_to_menu():
        GameFrame().set_scene(MenuScene())
    FightScene().init(go_next_round=go_next_round, back_to_menu=back_to_menu)


def start():
    init()
    GameFrame().set_scene(MenuScene())
    GameFrame().gui_loop()
