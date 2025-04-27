import math
import random
from typing import List, Tuple, Union
from pygame import time as pygame_time, mouse as pygame_mouse
from thread_management import ThreadManager
from gui_components import Scene, Component, TextButton, MouseEventAdapter, Surface, Label
from game_logic import ChooseCard, Battle, PlayerAttributeRecord
from game_resource import image, constants, audio
from game_element import Card, Player, CardEffect, PlayerEffect, player_factory, card_factory
from network import CommunicateData
from decorator import singleton
from .game import Game
from .delay import delay


class BattleMode:
    RANDOM: str = "random"
    EASY: str = "easy"
    NORMAL: str = "normal"
    HARD: str = "hard"
    SUPER_HARD: str = "super_hard"
    ASIAN: str = "asian"
    SERVER: str = "server"
    CLIENT: str = "client"


@singleton
class BattleScene(Scene):
    _selected_card_list: List[Card]
    _showing_card_list: List[Card]
    _card_detail: Component
    _current_round: int
    _local_player_name = "local player"
    _mode: str

    def __init__(self) -> None:
        super().__init__(image.get_image(image.BG_BATTLE_FIELD),
                         (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self._init_scene_attribute()

    def _init_scene_attribute(self):
        self._selected_card_list = []
        self._showing_card_list = []
        self._card_detail = None
        self._current_round = 0
        self._mode = None
        self.clear_component()

    def start_showing(self):
        self._mode = Game().get_battle_mode()
        ThreadManager().run_func_as_new_thread(target=self._battle_thread_func)

    def _battle_thread_func(self):
        if not self._check_connect():
            return

        player_creating_information = \
            Game().get_player_creating_information(Game().get_player_id())
        player_creating_information.name = self._local_player_name
        player = player_factory.get_player(player_creating_information)
        player_deck_card_id_list = Game().get_player_card_id_list()
        player.deck.extend([
            card_factory.get_card(card_id) for card_id in player_deck_card_id_list])

        if self._mode == BattleMode.SERVER:
            Game().get_server().send_player_and_deck(
                player_creating_information, player_deck_card_id_list)
            server_data = self._get_server_data(
                CommunicateData.PLAYER_AND_DECK)
            if server_data != None:
                enemy_creating_information, enemy_deck_card_id_list = server_data
            else:
                if not self._check_connect():
                    return
            enemy = player_factory.get_player(enemy_creating_information)
            enemy.deck.extend([
                card_factory.get_card(card_id) for card_id in enemy_deck_card_id_list])
        elif self._mode == BattleMode.CLIENT:
            Game().get_client().send_player_and_deck(
                player_creating_information, player_deck_card_id_list)
            client_data = self._get_client_data(
                CommunicateData.PLAYER_AND_DECK)
            if client_data != None:
                enemy_creating_information, enemy_deck_card_id_list = client_data
            else:
                if not self._check_connect():
                    return
            enemy = player_factory.get_player(enemy_creating_information)
            enemy.deck.extend([
                card_factory.get_card(card_id) for card_id in enemy_deck_card_id_list])
        elif self._mode == BattleMode.RANDOM:
            enemy_creating_information = \
                Game().get_player_creating_information(Game().get_random_enemy_id())
            enemy_creating_information.name = "random enemy"
            enemy = player_factory.get_player(enemy_creating_information)
            enemy.deck.extend([
                card_factory.get_card(card_id) for card_id in Game().get_random_enemy_card_id_list()])
        elif self._mode == BattleMode.EASY:
            enemy_creating_information = \
                player_factory.get_default_player_creating_information(4)
            enemy_creating_information.name = "KSP(easy)"
            enemy = player_factory.get_player(enemy_creating_information)
            enemy.deck.extend([
                card_factory.get_card(card_id) for card_id in Game().get_easy_enemy_card_id_list()])
        elif self._mode == BattleMode.NORMAL:
            enemy_creating_information = \
                player_factory.get_default_player_creating_information(4)
            enemy_creating_information.name = "KSP(normal)"
            enemy = player_factory.get_player(enemy_creating_information)
            enemy.deck.extend([
                card_factory.get_card(card_id) for card_id in Game().get_normal_enemy_card_id_list()])
        elif self._mode == BattleMode.HARD:
            enemy_creating_information = \
                player_factory.get_default_player_creating_information(4)
            enemy_creating_information.name = "KSP(hard)"
            enemy_creating_information.hp = (
                enemy_creating_information.max_hp + enemy_creating_information.hp) // 2
            enemy_creating_information.shield = (
                enemy_creating_information.max_shield + enemy_creating_information.shield) // 2
            enemy = player_factory.get_player(enemy_creating_information)
            enemy.deck.extend([
                card_factory.get_card(card_id) for card_id in Game().get_normal_enemy_card_id_list()])
        elif self._mode == BattleMode.SUPER_HARD:
            enemy_creating_information = \
                player_factory.get_default_player_creating_information(4)
            enemy_creating_information.name = "KSP(super hard)"
            enemy_creating_information.hp = enemy_creating_information.max_hp
            enemy_creating_information.shield = enemy_creating_information.max_shield
            enemy = player_factory.get_player(enemy_creating_information)
            enemy.deck.extend([
                card_factory.get_card(card_id) for card_id in Game().get_normal_enemy_card_id_list()])
        elif self._mode == BattleMode.ASIAN:
            enemy_creating_information = \
                player_factory.get_default_player_creating_information(4)
            enemy_creating_information.name = "KSP(asian)"
            enemy_creating_information.hp = enemy_creating_information.max_hp
            enemy_creating_information.shield = enemy_creating_information.max_shield
            enemy = player_factory.get_player(enemy_creating_information)
            enemy.deck = [card_factory.get_card(1000)]
        else:
            raise ValueError(f"mode is invalid. got {self._mode}")

        enemy.set_invert(True)
        self._draw_card(player, enemy, 1)

    def _draw_card(self, player: Player, enemy: Player, current_round: int):
        if not self._check_connect():
            return
        self.clear_component()
        self._current_round = current_round
        if self._mode == BattleMode.CLIENT:
            client_data = self._get_client_data(
                CommunicateData.DECK_AND_DRAWN_CARD_AND_DISCARD_CARD)
            if client_data != None:
                deck_card_id_list, player_drawn_card_id_list, player_discard_card_id_list = client_data
            else:
                if not self._check_connect():
                    return

            player.deck = \
                [card_factory.get_card(card_id)
                 for card_id in deck_card_id_list]
            player.drawn_card_list = \
                [card_factory.get_card(card_id)
                 for card_id in player_drawn_card_id_list]
            player_discard_card_list = \
                [card_factory.get_card(card_id)
                 for card_id in player_discard_card_id_list]
            player_drawn_card_list = player.drawn_card_list
        else:
            choose_card_logic = ChooseCard(player, enemy)
            player_drawn_card_list, enemy_drawn_card_list, player_discard_card_list, enemy_discard_card_list = choose_card_logic.do_draw_card(
                current_round)

        if self._mode == BattleMode.SERVER:
            Game().get_server().send_deck_and_drawn_card_list_and_discard_card_list([card.get_card_id() for card in enemy.deck],
                                                                                    [card.get_card_id(
                                                                                    ) for card in enemy_drawn_card_list],
                                                                                    [card.get_card_id() for card in enemy_discard_card_list])

        self._show_player_drawn_cards(
            player_drawn_card_list, player_discard_card_list)
        self._choose_attack_card(player, enemy, current_round)

    def _choose_attack_card(self, player: Player, enemy: Player, current_round: int):
        if not self._check_connect():
            return
        self._show_player_and_enemy(player, enemy)
        self._showing_card_list = []
        for card in player.drawn_card_list:
            self._showing_card_list.append(card)
            self.add_component(card)
        self._adjust_card_pos_to_spread_from_center(self._showing_card_list)

        select_card_mouse_handler = MouseEventAdapter(
            mouse_down=lambda event: self._handle_mouse_down_when_choosing_attack_card(),
            mouse_click=lambda event: self._handle_mouse_click_when_choosing_attack_card())
        self.add_mouse_handler(select_card_mouse_handler)

        def go_to_perform_card_attack():
            self.remove_mouse_handler(select_card_mouse_handler)
            for card in self._showing_card_list:
                card.remove_mask()
            player.attack_card_list = self._selected_card_list
            self._selected_card_list = []

            for card in player.attack_card_list:
                player.drawn_card_list.remove(card)

            if self._mode != BattleMode.SERVER:
                enemy.attack_card_list = random.sample(enemy.drawn_card_list,
                                                       k=min(current_round, len(enemy.drawn_card_list)))
                for card in enemy.attack_card_list:
                    enemy.drawn_card_list.remove(card)

            if self._mode == BattleMode.CLIENT:
                Game().get_client().send_attack_card_list(
                    [card.get_card_id() for card in player.attack_card_list])

            self.clear_component()
            ThreadManager().run_func_as_new_thread(target=self._perform_card_attack_thread_func, args=[
                player, enemy, current_round])

        confirm_btn = TextButton("確定")
        confirm_btn.set_pos((self.get_width() - confirm_btn.get_width(),
                            self.get_height() - confirm_btn.get_height()))
        confirm_btn.add_mouse_handler(MouseEventAdapter(
            mouse_click=lambda event: go_to_perform_card_attack()))
        self.add_component(confirm_btn)

    def _perform_card_attack_thread_func(self, player: Player, enemy: Player, current_round: int):
        if not self._check_connect():
            return
        if self._mode == BattleMode.SERVER:
            server_data = self._get_server_data(
                CommunicateData.ATTACK_DATA)
            if server_data != None:
                enemy_attack_card_id_list = server_data
            else:
                if not self._check_connect():
                    return
            enemy.attack_card_list = []
            for card_id in enemy_attack_card_id_list:
                for card in enemy.drawn_card_list:
                    if card_id == card.get_card_id():
                        enemy.attack_card_list.append(card)
                        break
            for card in enemy.attack_card_list:
                enemy.drawn_card_list.remove(card)

        if self._mode == BattleMode.CLIENT:
            client_data = self._get_client_data(CommunicateData.ROUND_RESULT)
            if client_data != None:
                winner_data, operation_record_data, attribute_record_data = client_data
            else:
                if not self._check_connect():
                    return

            if winner_data == "player":
                winner = player
            elif winner_data == "enemy":
                winner = enemy
            else:
                winner = None

            operation_record = {}
            for key, record_data in operation_record_data.items():
                attack_card_data, activate_card_effect_list, activate_player_effect_list, remove_player_effect_list = record_data
                if attack_card_data != None:
                    attack_card = card_factory.get_card(attack_card_data)
                else:
                    attack_card = None
                operation_record[key] = (
                    attack_card, activate_card_effect_list, activate_player_effect_list, remove_player_effect_list)

            attribute_record = attribute_record_data
        else:
            player.drawn_card_list.extend(
                card_factory.find_extra_card(player.attack_card_list))
            enemy.drawn_card_list.extend(
                card_factory.find_extra_card(enemy.attack_card_list))

            # do logic perform round
            winner, operation_record, attribute_record \
                = Battle(player, enemy).perform_round(current_round)

        if self._mode == BattleMode.SERVER:
            winner_data = None
            if winner is player:
                winner_data = "enemy"
            elif winner is enemy:
                winner_data = "player"

            operation_record_data = {}
            for key, record in operation_record.items():
                attack_card = None
                activate_card_effect_list = record[1]
                activate_player_effect_list = record[2]
                remove_player_effect_list = record[3]
                if record[0] != None:
                    attack_card = record[0].get_card_id()
                operation_record_data[key] = (
                    attack_card, activate_card_effect_list, activate_player_effect_list, remove_player_effect_list)

            attribute_record_data = [(enemy_attribute_record, player_attribute_record)
                                     for player_attribute_record, enemy_attribute_record in attribute_record]
            Game().get_server().send_round_result(
                (winner_data, operation_record_data, attribute_record_data))

        # init gui_palyer and gui_enemy
        player_attribute_record, enemy_attribute_record \
            = attribute_record.pop(0)
        self._show_player_and_enemy(
            player, enemy, player_attribute_record, enemy_attribute_record)
        delay(500)

        # show round start record
        if "round_start" in operation_record.keys():
            self._show_one_record(1000, 1000, 1000, Component(image.get_image(image.ROUND_START_SIGN)),
                                  player, enemy,
                                  operation_record["round_start"],
                                  attribute_record.pop(0))

        # show attack card record
        operation_record_list = []
        attack_card_attribute_record = []
        i = 0
        while not Game().get_close_flag().is_set():
            if f"attacked_card_result_{i}" in operation_record.keys():
                operation_record_list.append(
                    operation_record[f"attacked_card_result_{i}"])
                attack_card_attribute_record.append(attribute_record.pop(0))
                i += 1
            else:
                break
        self._show_attack_card_result(
            player, enemy, operation_record_list, attack_card_attribute_record)
        delay(1000)

        # show round end record
        if "round_end" in operation_record.keys():
            self._show_one_record(1000, 1000, 1000,
                                  Component(image.get_image(
                                      image.ROUND_END_SIGN)),
                                  player, enemy,
                                  operation_record["round_end"],
                                  attribute_record.pop(0))

        # handle round end
        self.clear_component()
        if winner is player:
            self._set_battle_end(player, True)
        elif winner is enemy:
            self._set_battle_end(enemy, False)
        elif current_round >= 4:
            if player.hp > enemy.hp:
                self._set_battle_end(player, True)
            else:
                self._set_battle_end(enemy, False)
        else:
            self._draw_card(player, enemy, current_round + 1)

    def _get_server_data(self, data_name: str):
        waiting_label = Label("等待對方...", constants.COLOR_WHITE)
        waiting_label_bg = Component(Surface(waiting_label.get_size()))
        self.add_component(waiting_label_bg)
        self.add_component(waiting_label)
        data = None
        while not Game().get_close_flag().is_set() and Game().get_server().is_connect():
            data = Game().get_server().get_data(data_name)
            if data != None:
                break
        self.remove_component(waiting_label_bg)
        self.remove_component(waiting_label)
        if isinstance(data, CommunicateData):
            return data.data
        else:
            return data

    def _get_client_data(self, data_name: str):
        waiting_label = Label("等待對方...", constants.COLOR_WHITE)
        waiting_label_bg = Component(Surface(waiting_label.get_size()))
        self.add_component(waiting_label_bg)
        self.add_component(waiting_label)
        data = None
        while not Game().get_close_flag().is_set() and Game().get_client().is_connect():
            data = Game().get_client().get_data(data_name)
            if data != None:
                break
        self.remove_component(waiting_label_bg)
        self.remove_component(waiting_label)
        if isinstance(data, CommunicateData):
            return data.data
        else:
            return data

    def _check_connect(self):
        if self._mode == BattleMode.SERVER:
            if not Game().get_server().is_connect():
                connect_lost_label = Label("連線已斷開", constants.COLOR_WHITE)
                connect_lost_label_bg = Component(
                    Surface(connect_lost_label.get_size()))
                self.add_component(connect_lost_label_bg)
                self.add_component(connect_lost_label)
                delay(3000)
                self.remove_component(connect_lost_label_bg)
                self.remove_component(connect_lost_label)
                self._init_scene_attribute()
                Game().remove_scene(self)
                return False
        elif self._mode == BattleMode.CLIENT:
            if not Game().get_client().is_connect():
                connect_lost_label = Label("連線已斷開", constants.COLOR_WHITE)
                connect_lost_label_bg = Component(
                    Surface(connect_lost_label.get_size()))
                self.add_component(connect_lost_label_bg)
                self.add_component(connect_lost_label)
                delay(3000)
                self.remove_component(connect_lost_label_bg)
                self.remove_component(connect_lost_label)
                self._init_scene_attribute()
                Game().remove_scene(self)
                return False
        return True

    def _show_attack_card_result(self, player: Player, enemy: Player,
                                 operation_record: List[Tuple[Card, List[CardEffect], List[PlayerEffect], List[PlayerEffect]]],
                                 attribute_record: List[Tuple[PlayerAttributeRecord, PlayerAttributeRecord]]):
        effect_sound = audio.get_sound(audio.EFFECT_CARD_ATTACK)
        show_time_list = [4941, 11268, 17776, 24012,
                          30703, 40216, 46588, 52960, 62655]
        attack_card_bg_jump_up_time = 100
        is_attack_card_bg_shown = False
        switch_bgm_fade_time = 1000
        showing_card_index = 0
        Game().pause_bgm(switch_bgm_fade_time)
        effect_sound.play(-1, fade_ms=switch_bgm_fade_time)
        start_time = pygame_time.get_ticks()

        while not Game().get_close_flag().is_set():
            current_time = pygame_time.get_ticks()
            elapsed_time = current_time - start_time

            if (len(operation_record) == 0 and len(attribute_record) == 0) or (not Game().is_running()):
                break
            if (elapsed_time >= show_time_list[showing_card_index] - attack_card_bg_jump_up_time) and not is_attack_card_bg_shown:
                ThreadManager().run_func_as_new_thread(target=self._show_attack_card_bg_thread_func,
                                                       args=[attack_card_bg_jump_up_time, 4000])
                is_attack_card_bg_shown = True
            if elapsed_time >= show_time_list[showing_card_index]:
                operation = operation_record.pop(0)
                attack_card, activated_card_effect_list, activated_player_effect_list, removed_player_effect \
                    = operation
                attribute_record_pair = attribute_record.pop(0)
                self._show_one_record(2000, 2000, 0,
                                      attack_card, player, enemy,
                                      operation, attribute_record_pair)
                showing_card_index += 1
                is_attack_card_bg_shown = False
            if showing_card_index >= len(show_time_list):
                showing_card_index -= len(show_time_list)
                for i in range(len(show_time_list)):
                    show_time_list[i] += int(effect_sound.get_length() * 1000)

        effect_sound.fadeout(switch_bgm_fade_time)
        Game().resume_bgm(switch_bgm_fade_time)

    def _show_player_and_enemy(self, player: Player, enemy: Player,
                               player_attribute_record: Union[PlayerAttributeRecord, None] = None, enemy_attribute_record: Union[PlayerAttributeRecord, None] = None):
        player.set_x(
            self.get_centerx() - player.get_width()//2)
        player.set_y(
            self.get_height() - player.get_height())
        self.add_component(player)
        enemy.set_x(
            self.get_centerx() - enemy.get_width()//2)
        enemy.set_y(0)
        self.add_component(enemy)
        if player_attribute_record and enemy_attribute_record:
            self._set_gui_player_attribute(player,
                                           player_attribute_record)
            self._set_gui_player_attribute(enemy,
                                           enemy_attribute_record)

    def _show_one_record(self, delay_after_show_comp: int, delay_after_set_player_attribute: int, delay_after_remove_comp: int,
                         show_comp: Component, player: Player, enemy: Player,
                         operation: Tuple[Union[Card, None], Union[List[CardEffect], None], List[PlayerEffect], List[PlayerEffect]],
                         attribute_record: Tuple[PlayerAttributeRecord, PlayerAttributeRecord]):
        card, activated_card_effect_list, activated_player_effect_list, remove_player_effect_list = operation
        player_attribute_record, enemy_attribute_record = attribute_record
        show_comp.set_center((self.get_width()//2,
                              self.get_height()//2))
        self.add_component(show_comp)
        effect_y = 0
        activate_effect_comp_list = []
        for effect in activated_player_effect_list:
            temp_effect_comp = Component(effect.get_background())
            temp_effect_comp.set_y(effect_y)
            self.add_component(temp_effect_comp)
            activate_effect_comp_list.append(temp_effect_comp)
            effect_y += effect.get_height()
        if type(show_comp) is Card:
            show_comp.play_attack_sound()
        delay(delay_after_show_comp)
        self._set_gui_player_attribute(player, player_attribute_record)
        self._set_gui_player_attribute(enemy, enemy_attribute_record)
        delay(delay_after_set_player_attribute)
        self.remove_component(show_comp)
        for effect_comp in activate_effect_comp_list:
            self.remove_component(effect_comp)
        delay(delay_after_remove_comp)

    def _show_attack_card_bg_thread_func(self, attack_card_bg_jump_up_time: int, attack_card_bg_remain_time: int):
        attack_background = Component(
            image.get_image(image.BATTLE_CARD_ATTACK_BG))
        self.add_component(attack_background)
        attack_background.set_center(
            (self.get_width()//2, self.get_height()//2))
        original_size = attack_background.get_size()
        original_pos = attack_background.get_pos()
        attack_background.set_size((0, 0))
        attack_card_bg_jump_up_time_per_step = attack_card_bg_jump_up_time//5
        attack_card_bg_width_per_step = original_size[0]//5
        attack_card_bg_height_per_step = original_size[1]//5
        for i in range(1, 5):
            self._move_and_grow_comp(attack_background,
                                     attack_card_bg_jump_up_time_per_step,
                                     (attack_card_bg_width_per_step * i,
                                      attack_card_bg_height_per_step * i),
                                     original_pos)
            attack_background.set_background(
                image.get_image(image.BATTLE_CARD_ATTACK_BG))
        self._move_and_grow_comp(attack_background,
                                 attack_card_bg_jump_up_time - attack_card_bg_jump_up_time_per_step * 4,
                                 original_size,
                                 original_pos)
        attack_background.set_background(
            image.get_image(image.BATTLE_CARD_ATTACK_BG))
        delay(attack_card_bg_remain_time)
        self.remove_component(attack_background)

    def _move_and_grow_comp(self, comp: Component, duration: int, target_size: Tuple[int, int], target_pos: Tuple[int, int]) -> None:
        def lerp(start: int, end: int, alpha: float):
            return math.ceil((1 - alpha) * start + alpha * end)
        start_pos = comp.get_pos()
        start_size = comp.get_size()
        start_time = pygame_time.get_ticks()

        while not Game().get_close_flag().is_set():
            current_time = pygame_time.get_ticks()
            elapsed_time = current_time - start_time

            if (elapsed_time >= duration) or (not Game().is_running()):
                comp.set_pos(target_pos)
                comp.set_size(target_size)
                break

            alpha = elapsed_time / duration
            comp.set_pos((lerp(start_pos[0], target_pos[0], alpha),
                         lerp(start_pos[1], target_pos[1], alpha)))
            comp.set_size((lerp(start_size[0], target_size[0], alpha),
                          lerp(start_size[1], target_size[1], alpha)))

    def _set_battle_end(self, winner: Player, is_player_win: bool):
        self.add_component(winner)
        if is_player_win:
            win_sign = Component(image.get_image(image.WIN_SIGN))
            win_sign.set_center(
                (self.get_width()//2, self.get_height()//2))
            self.add_component(win_sign)
            win_sound = audio.get_sound(audio.EFFECT_WINING)
            win_sound.play()
            delay(int(win_sound.get_length()*1000))
            delay(500)
            if self._mode == BattleMode.EASY:
                Game().add_user_point(1)
            elif self._mode == BattleMode.NORMAL:
                Game().add_user_point(3)
            elif self._mode == BattleMode.HARD:
                Game().add_user_point(4)
            elif self._mode == BattleMode.SUPER_HARD:
                Game().add_user_point(5)
            elif self._mode == BattleMode.ASIAN:
                Game().add_user_point(7414)
            elif self._mode == BattleMode.RANDOM:
                Game().add_user_point(random.randint(3, 5))
            self._init_scene_attribute()
            Game().remove_scene(self)
        else:
            lose_sign = Component(image.get_image(image.LOSE_SIGN))
            lose_sign.set_center(
                (self.get_width()//2, self.get_height()//2))
            self.add_component(lose_sign)
            lose_sound = audio.get_sound(audio.EFFECT_LOSING)
            lose_sound.play()
            delay(int(lose_sound.get_length()*1000))
            delay(500)
            self._init_scene_attribute()
            Game().remove_scene(self)

    def _set_gui_player_attribute(self, player: Player, attribute_record: PlayerAttributeRecord):
        player.set_hp_bar_value(attribute_record.hp)
        player.set_shield_bar_value(attribute_record.shield)
        player.set_max_hp_bar_value(attribute_record.max_hp)
        player.set_max_shield_bar_value(attribute_record.max_shield)

    def _handle_mouse_down_when_choosing_attack_card(self):
        mouse_pos = pygame_mouse.get_pos()
        if self._card_detail:
            self.remove_component(self._card_detail)
        for card in self._showing_card_list:
            if card.is_collide(mouse_pos):
                self._card_detail = card_factory.get_card_detail(
                    card.get_card_id())
                self.add_component(self._card_detail)
                break

    def _handle_mouse_click_when_choosing_attack_card(self):
        mouse_pos = pygame_mouse.get_pos()
        for card in self._showing_card_list:
            if card.is_collide(mouse_pos):
                if card in self._selected_card_list:
                    audio.get_sound(audio.EFFECT_SELECT_CARD).play()
                    self._selected_card_list.remove(card)
                    card.remove_mask()
                elif len(self._selected_card_list) < self._current_round:
                    audio.get_sound(audio.EFFECT_SELECT_CARD).play()
                    self._selected_card_list.append(card)
                break
        for i, selected_card in enumerate(self._selected_card_list):
            selected_card.set_mask(f"{i + 1}")

    def _adjust_card_pos_to_spread_from_center(self, card_list: List[Card], card_spacing: int = 20):
        if len(card_list) == 1:
            card_list[0].set_center(self.get_center())
        elif len(card_list) > 1:
            max_cards_per_column = 2
            max_cards_per_line = math.ceil(
                len(card_list) / max_cards_per_column)

            leftmost_centerx = self.get_width()//2 - (max_cards_per_line / 2 - 0.5) * \
                (card_list[0].get_width() + card_spacing)

            topmost_centery = self.get_height()//2 - (max_cards_per_column / 2 - 0.5) * \
                (card_list[0].get_height() + card_spacing)

            for i, card in enumerate(card_list):
                line = i // max_cards_per_line
                card.set_center((leftmost_centerx + (i % max_cards_per_line) * (
                    card.get_width() + card_spacing), topmost_centery + line * (card.get_height() + card_spacing)))

    def _show_player_drawn_cards(self, player_drawn_card_list: List[Card], player_discard_card_list: List[Card]):
        begin_sound = audio.get_sound(audio.EFFECT_DRAW_CARD_BEGIN)
        begin_sound.play()
        delay(int(begin_sound.get_length()*1000))
        for card in player_drawn_card_list:
            self._show_one_player_drawn_card(card, False)
        for card in player_discard_card_list:
            self._show_one_player_drawn_card(card, True)

    def _show_one_player_drawn_card(self, card: Card, is_discard: bool):
        card.set_center((self.get_width()//2, self.get_height()//2))
        audio.get_sound(audio.EFFECT_DRAW_CARD).play()
        self.add_component(card)
        if is_discard:
            discard_mask = Component(image.get_image(image.CARD_DISCARD_MASK))
            discard_mask.set_center(
                (self.get_width()//2, self.get_height()//2))
            delay(500)
            self.add_component(discard_mask)
            delay(500)
            self.remove_component(discard_mask)
        else:
            delay(1000)
        self.remove_component(card)
        delay(100)
