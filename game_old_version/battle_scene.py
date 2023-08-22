import math
import random
from typing import Callable, List, Tuple, Union

from gui_components import Scene, Component, Label, TextButton, Surface, MouseEventAdapter
from pygame import time as pygame_time, mouse as pygame_mouse
from pygame.mixer import Sound
from gui_components.box import Box
from resource import audio, image, constants
from threading import Thread

from .decorator import singleton
from .game_frame import GameFrame
from .card import Card
from .player import Player
from .player_effect import PlayerEffect
from . import card_effect, card_factory

_get_player: Callable[[], Player]
_get_enemy: Callable[[], Player]


def init(get_player: Callable[[], Player], get_enemy: Callable[[], Player]):
    global _get_player
    global _get_enemy
    _get_player = get_player
    _get_enemy = get_enemy


@singleton
class ChooseCardScene(Scene):
    _player_card_list: List[Card]
    _player_selected_card_list: List[Card]
    _enemy_card_list: List[Card]
    _enemy_selected_card_list: List[Card]
    _card_mask: List[Component]
    _player: Player
    _enemy: Player
    _round_count: int
    _confirm_btn: Component
    _card_detail: Component

    def __init__(self) -> None:
        super().__init__(image.get_image(image.BG_BATTLE_FIELD),
                         (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self._player_card_list = []
        self._player_selected_card_list = []
        self._enemy_card_list = []
        self._enemy_selected_card_list = []
        self._card_mask = []
        self._player = None
        self._enemy = None
        self._round_count = None
        self._confirm_btn = None
        self._card_detail = None
        self.add_mouse_handler(MouseEventAdapter(mouse_down=lambda event: self._mouse_down(),
                                                 mouse_click=lambda event: self._mouse_click()))

    def init(self, go_to_fight_scene: Callable[[], None]):
        def go_fight_with_remove_card():
            self._enemy_selected_card_list.extend(random.sample(self._enemy_card_list,
                                                                k=min(self._round_count, len(self._enemy_card_list))))
            for card in self._player_selected_card_list:
                self._player_card_list.remove(card)
                self.remove_component(card)
            for card in self._enemy_selected_card_list:
                self._enemy_card_list.remove(card)

            self.clear_component()
            go_to_fight_scene()
        self._confirm_btn = TextButton("確定")
        self._confirm_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: go_fight_with_remove_card()))
        self._confirm_btn.set_pos((self.get_rect().right - self._confirm_btn.get_size()[0],
                                   self.get_rect().bottom - self._confirm_btn.get_size()[1]))
        self.add_component(self._confirm_btn)

    def start(self, is_battle_start: bool) -> None:
        self.clear_component()

        if is_battle_start:
            self._round_count = 1
            self._player_card_list = []
            self._enemy_card_list = []
            self._player = _get_player()
            self._enemy = _get_enemy()
            self._enemy.set_rotate(True)
        else:
            self._round_count += 1
            self._player_card_list = FightScene().get_player_remain_card_list()
            self._enemy_card_list = FightScene().get_enemy_remain_card_list()
            self._player = FightScene().get_player()
            self._enemy = FightScene().get_enemy()
        self._player_selected_card_list = []
        self._enemy_selected_card_list = []
        self._remove_card_mask()

        self._draw_crad()
        self.add_component(self._confirm_btn)

        for card in self._player_card_list:
            self.add_component(card)
        self._auto_set_card_pos()

    def get_player(self):
        return self._player

    def get_enemy(self):
        return self._enemy

    def get_player_select_card_list(self):
        return self._player_selected_card_list

    def get_player_remain_card_list(self):
        return self._player_card_list

    def get_enemy_select_card_lsit(self):
        return self._enemy_selected_card_list

    def get_enemy_remain_card_list(self):
        return self._enemy_card_list

    def get_current_round(self):
        return self._round_count

    def _draw_crad(self):
        begin_sound = audio.get_sound(audio.EFFECT_DRAW_CARD_BEGIN)
        begin_sound.play()
        pygame_time.delay(int(begin_sound.get_length()*1000))
        if self._round_count == 1:
            player_draw_card_list = self._player.draw_card(2)
            for card in player_draw_card_list:
                self._show_one_card(card, False)
            self._player_card_list.extend(player_draw_card_list)
            self._enemy_card_list.extend(self._enemy.draw_card(2))
        player_draw_card_list = self._player.draw_card(self._round_count)
        self._player_card_list.extend(player_draw_card_list)
        self._enemy_card_list.extend(self._enemy.draw_card(self._round_count))
        for _ in range(len(self._player_card_list) - 8):
            self._player_card_list.pop()
        for _ in range(len(self._enemy_card_list) - 8):
            self._enemy_card_list.pop()
        for card in player_draw_card_list:
            if card in self._player_card_list:
                self._show_one_card(card, False)
            else:
                self._show_one_card(card, True)

    def _show_one_card(self, card: Card, is_discard: bool):
        card.set_center((self.get_width()//2, self.get_height()//2))
        audio.get_sound(audio.EFFECT_DRAW_CARD).play()
        self.add_component(card)
        if is_discard:
            discard_mask = Component(image.get_image(
                image.CARD_DISCARD_MASK))
            discard_mask.set_center(
                (self.get_width()//2, self.get_height()//2))
            pygame_time.delay(500)
            self.add_component(discard_mask)
            pygame_time.delay(500)
            self.remove_component(discard_mask)
        else:
            pygame_time.delay(1000)
        self.remove_component(card)
        pygame_time.delay(100)

    def _mouse_down(self):
        mouse_pos = pygame_mouse.get_pos()
        for card in self._player_card_list:
            if card.is_collide(mouse_pos):
                if self._card_detail:
                    self.remove_component(self._card_detail)
                self._card_detail = card_factory.get_detail(card.get_id())
                self.add_component(self._card_detail)
                break

    def _mouse_click(self):
        mouse_pos = pygame_mouse.get_pos()
        for card in self._player_card_list:
            if card.is_collide(mouse_pos):
                if card in self._player_selected_card_list:
                    Sound.play(audio.get_sound(
                        audio.EFFECT_SELECT_CARD))
                    self._player_selected_card_list.remove(card)
                elif len(self._player_selected_card_list) < self._round_count:
                    Sound.play(audio.get_sound(
                        audio.EFFECT_SELECT_CARD))
                    self._player_selected_card_list.append(card)
                break
        self._remove_card_mask()
        self._add_card_mask()

    def _auto_set_card_pos(self, card_spacing: int = 20):
        if len(self._player_card_list) == 1:
            for card in self._player_card_list:
                card.set_center(self.get_center())
        elif len(self._player_card_list) > 1:
            max_cards_per_column = 2
            max_cards_per_line = math.ceil(
                len(self._player_card_list) / max_cards_per_column)

            leftmost_centerx = self.get_centerx() - (max_cards_per_line / 2 - 0.5) * \
                (self._player_card_list[0].get_width()+card_spacing)

            topmost_centery = self.get_centery() - (max_cards_per_column / 2 - 0.5) * \
                (self._player_card_list[0].get_height() + card_spacing)

            for i, card in enumerate(self._player_card_list):
                line = i // max_cards_per_line
                card.set_center((leftmost_centerx + (i % max_cards_per_line) * (
                    card.get_width() + card_spacing), topmost_centery + line * (card.get_height() + card_spacing)))

    def _remove_card_mask(self) -> None:
        for mask in self._card_mask:
            self.remove_component(mask)
        self._card_mask.clear()

    def _add_card_mask(self) -> None:
        def create_card_mask(text: str, size: Tuple[int, int]) -> Box:
            if len(self._player_card_list) > 0:
                mask = Box(Surface(size))
                mask.set_alpha(constants.CARD_MASK_ALPHA)
                mask.fill(constants.COLOR_GRAY)
                label = Label(text, constants.COLOR_WHITE)
                label.set_center((mask.get_width()//2, mask.get_height()//2))
                mask.add_component(label)
                return mask
            return Component(Surface((0, 0)))

        for i, card in enumerate(self._player_selected_card_list):
            mask = create_card_mask(str(i + 1), card.get_size())
            mask.set_center(card.get_center())
            self.add_component(mask)
            self._card_mask.append(mask)


@singleton
class FightScene(Scene):
    _player_card_list: List[Card]
    _player_remain_card_list: List[Card]
    _enemy_card_list: List[Card]
    _enemy_remain_card_list: List[Card]
    _player: Player
    _enemy: Player
    _round_count: int
    _go_next_round: Callable[[], None]
    _back_to_menu: Callable[[], None]
    _effect_icon_list: List[Component]

    def __init__(self) -> None:
        super().__init__(image.get_image(image.BG_BATTLE_FIELD))
        self._player_card_list = []
        self._player_remain_card_list = []
        self._enemy_card_list = []
        self._player = None
        self._enemy = None
        self._round_count = 0
        self._go_next_round = None
        self._back_to_menu = None
        self._effect_icon_list = []

    def init(self, go_next_round: Callable[[], None], back_to_menu: Callable[[], None]) -> None:
        self._go_next_round = go_next_round
        self._back_to_menu = back_to_menu

    def fight(self):
        self.clear_component()

        self._effect_icon_list = []
        self._round_count = ChooseCardScene().get_current_round()
        self._player_remain_card_list = ChooseCardScene().get_player_remain_card_list()
        self._enemy_remain_card_list = ChooseCardScene().get_enemy_remain_card_list()

        self._player_card_list = ChooseCardScene().get_player_select_card_list()
        self._enemy_card_list = ChooseCardScene().get_enemy_select_card_lsit()
        self._player = ChooseCardScene().get_player()
        self._enemy = ChooseCardScene().get_enemy()

        self._player.check_effect()
        self._player.set_center(
            (self.get_width()//2, self._player.get_centery()))
        self._player.set_y(self.get_height()-self._player.get_height())
        self.add_component(self._player)

        self._enemy.check_effect()
        self._enemy.set_center(
            (self.get_width()//2, self._enemy.get_centery()))
        self._enemy.set_y(0)
        self.add_component(self._enemy)

        card_effect.find_extra_card(
            self._player_card_list, self._player_remain_card_list)
        card_effect.find_extra_card(
            self._enemy_card_list, self._enemy_remain_card_list)

        self._perform_all_card_attack(
            [4941, 11268, 17776, 24012, 30703, 40216, 46588, 52960, 62655])

    def get_player(self):
        return self._player

    def get_enemy(self):
        return self._enemy

    def get_player_attack_card_list(self):
        return self._player_card_list

    def get_player_remain_card_list(self):
        return self._player_remain_card_list

    def get_enemy_attack_card_list(self):
        return self._enemy_card_list

    def get_enemy_remain_card_list(self):
        return self._enemy_remain_card_list

    def get_current_round(self):
        return self._round_count

    def add_effect_icon(self, icon: Component):
        if icon in self._effect_icon_list:
            icon = Component(icon.get_background())
        if len(self._effect_icon_list) > 0:
            icon.set_y(self._effect_icon_list[-1].get_bottom())
        self.add_component(icon)
        self._effect_icon_list.append(icon)
        return icon

    def remove_effect_icon(self, icon: Component):
        self.remove_component(icon)
        if icon in self._effect_icon_list:
            self._effect_icon_list.remove(icon)

    def _find_winner(self, is_battle_end: bool) -> Union[Player, None]:
        if self._enemy.get_hp_value() <= 0:
            return self._player
        if self._player.get_hp_value() <= 0:
            return self._enemy
        elif is_battle_end:
            if self._enemy.get_hp_value() < self._player.get_hp_value():
                return self._player
            else:
                return self._enemy
        return None

    def _move_and_grow_comp(self, comp: Component, duration: int, target_size: Tuple[int, int], target_pos: Tuple[int, int]) -> None:
        def lerp(start: int, end: int, alpha: float):
            return math.ceil((1 - alpha) * start + alpha * end)
        start_pos = comp.get_pos()
        start_size = comp.get_size()
        start_time = pygame_time.get_ticks()

        while True:
            current_time = pygame_time.get_ticks()
            elapsed_time = current_time - start_time

            if elapsed_time >= duration:
                comp.set_pos(target_pos)
                comp.set_size(target_size)
                break

            alpha = elapsed_time / duration
            comp.set_pos((lerp(start_pos[0], target_pos[0], alpha),
                         lerp(start_pos[1], target_pos[1], alpha)))
            comp.set_size((lerp(start_size[0], target_size[0], alpha),
                          lerp(start_size[1], target_size[1], alpha)))

    def _load_card_attack_background_per_millisecond(self, attack_background: Component, milliseconds: int, duration: int) -> None:
        start_time = pygame_time.get_ticks()
        while True:
            current_time = pygame_time.get_ticks()
            elapsed_time = current_time - start_time

            if elapsed_time >= duration:
                attack_background.set_background(
                    image.get_image(image.BATTLE_CARD_ATTACK_BG))
                break
            if elapsed_time >= milliseconds:
                attack_background.set_background(
                    image.get_image(image.BATTLE_CARD_ATTACK_BG))

    def _show_card_jump_up_background(self, effect_milliseconds: int, duration: int) -> None:
        attack_background = Component(
            image.get_image(image.BATTLE_CARD_ATTACK_BG))
        self.add_component(attack_background)
        attack_background.set_center(self.get_center())
        original_size = attack_background.get_size()
        original_pos = attack_background.get_pos()
        attack_background.set_size((0, 0))
        Thread(target=self._load_card_attack_background_per_millisecond,
               args=[attack_background, 10, effect_milliseconds]).start()
        self._move_and_grow_comp(attack_background, effect_milliseconds,
                                 original_size,
                                 original_pos)
        pygame_time.delay(duration - effect_milliseconds)
        self.remove_component(attack_background)

    def _play_card_attack_sound(self, fade_in: int, fade_out: int, maxtime: int) -> None:
        sound = audio.get_sound(audio.EFFECT_CARD_ATTACK)
        sound.play(fade_ms=fade_in, maxtime=maxtime)
        pygame_time.delay(int(maxtime - fade_out))
        sound.fadeout(fade_out)

    def _perform_one_card_attack(self, is_from_player: bool, card: Card, card_jump_up_time: int, card_showing_time: int) -> None:
        Thread(target=self._show_card_jump_up_background,
               args=[card_jump_up_time, card_showing_time]).start()
        pygame_time.delay(card_jump_up_time)
        card.set_center((self.get_width()//2, self.get_height()//2))
        self.add_component(card)
        card_remain_time = card_showing_time - card_jump_up_time
        pygame_time.delay(500)
        self._do_player_effect_no_delay(PlayerEffect.BEFORE_CARD)
        card_effect.do_effect(card.get_effect_id(), is_from_player)
        player_effect_delay = 500
        is_do_effect = self._do_player_effect_with_delay(PlayerEffect.AFTER_CARD,
                                                         player_effect_delay)
        if is_do_effect:
            pygame_time.delay(card_remain_time - 500 - player_effect_delay)
        else:
            pygame_time.delay(card_remain_time - 500)
        self.remove_component(card)

    def _set_battle_end(self, is_player_win: bool) -> None:
        if is_player_win:
            self.clear_component()
            self.add_component(self._player)
            winner_sign = Component(
                image.get_image(image.WIN_SIGN))
            winner_sign.set_center((self.get_width()//2, self.get_height()//2))
            self.add_component(winner_sign)
            audio.get_sound(audio.EFFECT_WINING).play()
        else:
            self.clear_component()
            self.add_component(self._enemy)
            loser_sign = Component(
                image.get_image(image.LOSE_SIGN))
            loser_sign.set_center((self.get_width()//2, self.get_height()//2))
            self.add_component(loser_sign)
            audio.get_sound(audio.EFFECT_LOSING).play()
        pygame_time.delay(6000)
        self._back_to_menu()

    def _handle_round_end(self) -> None:
        if self._round_count >= 4:
            winner = self._find_winner(is_battle_end=True)
            self._set_battle_end(is_player_win=(winner is self._player))
        else:
            winner = self._find_winner(is_battle_end=False)
            if winner:
                self._set_battle_end(is_player_win=(winner is self._player))
            elif self._go_next_round:
                self._go_next_round()

    def _random_choose_if_player_attack(self) -> bool:
        if len(self._player_card_list) == 0:
            return False
        elif len(self._enemy_card_list) == 0:
            return True
        else:
            return random.randint(0, 1) == 1

    def _do_player_effect_no_delay(self, timing: str):
        self._player.do_effect("", 0, timing)
        self._enemy.do_effect("", 0, timing)

    def _do_player_effect_with_delay(self, timing: str, delay: int):
        if self._player.is_contain_effect(timing) and self._enemy.is_contain_effect(timing):
            pygame_time.delay(delay)
            self._player.do_effect("", 0, timing)
            self._enemy.do_effect("", 0, timing)
            return True
        elif self._enemy.is_contain_effect(timing):
            pygame_time.delay(delay)
            self._enemy.do_effect("", 0, timing)
            return True
        elif self._player.is_contain_effect(timing):
            pygame_time.delay(delay)
            self._player.do_effect("", 0, timing)
            return True
        return False

    def _perform_all_card_attack(self, card_show_time: List[int]) -> None:
        effect_sound = audio.get_sound(audio.EFFECT_CARD_ATTACK)
        card_show_time_list_length = len(card_show_time)
        current_showing_card_index = 0
        card_jump_up_time = 200
        GameFrame().pause_bgm(1000)
        self._do_player_effect_with_delay(PlayerEffect.BEFORE_ROUND, 1000)
        start_time = pygame_time.get_ticks()
        effect_sound.play(-1)

        while True:
            current_time = pygame_time.get_ticks()
            elapsed_time = current_time - start_time

            if len(self._player_card_list) == 0 and len(self._enemy_card_list) == 0:
                break
            elif self._find_winner(is_battle_end=False):
                break
            elif elapsed_time >= card_show_time[current_showing_card_index] - card_jump_up_time:
                if self._random_choose_if_player_attack():
                    self._perform_one_card_attack(True, self._player_card_list[0],
                                                  card_jump_up_time, 3500)
                    self._player_card_list.remove(self._player_card_list[0])
                else:
                    self._perform_one_card_attack(False, self._enemy_card_list[0],
                                                  card_jump_up_time, 3500)
                    self._enemy_card_list.remove(self._enemy_card_list[0])
                current_showing_card_index += 1
            if current_showing_card_index == card_show_time_list_length:
                current_showing_card_index -= card_show_time_list_length
                for i in range(card_show_time_list_length):
                    card_show_time[i] += int(effect_sound.get_length() * 1000)

        effect_sound.fadeout(1000)
        self._do_player_effect_with_delay(PlayerEffect.AFTER_ROUND, 1000)
        self._player.check_effect()
        self._enemy.check_effect()
        pygame_time.delay(1000)
        GameFrame().resume_bgm(1000)
        self._handle_round_end()
