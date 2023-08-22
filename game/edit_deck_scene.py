import math
from thread_management import ThreadManager
from typing import List, Tuple
from gui_components import Scene, RoundButton, TextButton, MouseEventAdapter, Component, BaseButton
from game_resource import audio, image, constants
from pygame import mouse as pygame_mouse
from game_element import Card, card_factory
from decorator import singleton

from .game import Game


@singleton
class EditDeckScene(Scene):
    _selected_card_id_list: List[int]
    _page_list: List[List[Card]]
    _current_page: int
    _card_detail: Component
    _btn_list: List[BaseButton]
    _last_mouse_press: Tuple[bool, bool, bool]

    def __init__(self) -> None:
        super().__init__(image.get_image(image.BG_MENU),
                         (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self._selected_card_id_list = []
        self._page_list = []
        self._current_page = 0
        self._card_detail = None
        self._btn_list = []
        self._last_mouse_press = (False, False, False)
        self.add_mouse_handler(MouseEventAdapter(
            mouse_down=lambda event: self._handle_mouse_down(),
            mouse_click=lambda event: self._handle_mouse_click()))
        
        left_btn = RoundButton(image.get_image(image.BTN_LEFT_UP),
                               image.get_image(image.BTN_LEFT_DOWN))
        left_btn.set_x(self.get_centerx() - left_btn.get_width() - 10)
        left_btn.set_y(self.get_height() - left_btn.get_height())
        left_btn.add_mouse_handler(MouseEventAdapter(
            mouse_click=lambda event: self._go_left_page()))
        right_btn = RoundButton(image.get_image(image.BTN_RIGHT_UP),
                                image.get_image(image.BTN_RIGHT_DOWN))
        right_btn.set_x(self.get_centerx() + 10)
        right_btn.set_y(self.get_height() - right_btn.get_height())
        right_btn.add_mouse_handler(MouseEventAdapter(
            mouse_click=lambda event: self._go_right_page()))
        self.add_component(left_btn)
        self.add_component(right_btn)
        self._btn_list.append(left_btn)
        self._btn_list.append(right_btn)

        def back_to_menu_with_setting_player_card_id_list():
            Game().set_player_card_id_list(
                [card_id for card_id in self._selected_card_id_list])
            Game().remove_scene(self)
        confirm_btn = TextButton("確定")
        confirm_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: back_to_menu_with_setting_player_card_id_list()))
        confirm_btn.set_pos((self.get_width() - confirm_btn.get_width(),
                             self.get_height() - confirm_btn.get_height()))
        self.add_component(confirm_btn)
        self._btn_list.append(confirm_btn)

    def start_showing(self):
        ThreadManager().run_func_as_new_thread(target=self._show_all_card_thread_func)

    def _show_all_card_thread_func(self):
        self.clear_component()
        all_card_list \
            = [card_factory.get_card(card_id) for card_id in Game().get_unlock_card_id_list()]
        self._page_list = [all_card_list[i:i + 8]
                           for i in range(0, len(all_card_list), 8)]
        self._selected_card_id_list \
            = [card_id for card_id in Game().get_player_card_id_list()]
        self._turn_to_page(0)

    def _handle_mouse_down(self):
        if self._card_detail:
            self.remove_component(self._card_detail)
        mouse_pos = pygame_mouse.get_pos()
        self._last_mouse_press = pygame_mouse.get_pressed()
        for card in self._page_list[self._current_page]:
            if card.is_collide(mouse_pos):
                self._card_detail = card_factory.get_card_detail(
                    card.get_card_id())
                self.add_component(self._card_detail)
                break

    def _handle_mouse_click(self):
        mouse_pos = pygame_mouse.get_pos()
        mouse_left, _, mouse_right = self._last_mouse_press
        for card in self._page_list[self._current_page]:
            if card.is_collide(mouse_pos):
                if mouse_left:
                    if len(self._selected_card_id_list) < 20 and self._selected_card_id_list.count(card.get_card_id()) < 2:
                        audio.get_sound(audio.EFFECT_SELECT_CARD).play()
                        self._selected_card_id_list.append(card.get_card_id())
                elif mouse_right and self._selected_card_id_list.count(card.get_card_id()) > 0:
                    audio.get_sound(audio.EFFECT_SELECT_CARD).play()
                    self._selected_card_id_list.remove(card.get_card_id())
                break
        self._set_showing_card_mask()

    def _set_showing_card_mask(self):
        for card in self._page_list[self._current_page]:
            selected_count = self._selected_card_id_list.count(
                card.get_card_id())
            if selected_count == 0:
                card.remove_mask()
            else:
                card.set_mask(str(selected_count))

    def _go_left_page(self) -> None:
        if self._current_page > 0:
            self._turn_to_page(self._current_page - 1)

    def _go_right_page(self) -> None:
        if self._current_page < len(self._page_list) - 1:
            self._turn_to_page(self._current_page + 1)

    def _turn_to_page(self, page: int) -> None:
        self.clear_component()
        for btn in self._btn_list:
            self.add_component(btn)
        self._current_page = page
        for card in self._page_list[self._current_page]:
            self.add_component(card, 0)
        self._adjust_card_pos_to_spread_from_center(self._page_list[page])
        self._set_showing_card_mask()

    def _adjust_card_pos_to_spread_from_center(self, card_list: List[Card], card_spacing: int = 20):
        if len(card_list) == 1:
            card_list[0].set_center(self.get_center())
        elif len(card_list) > 1:
            max_cards_per_column = 2
            max_cards_per_line = math.ceil(
                len(card_list) / max_cards_per_column)

            leftmost_centerx = self.get_width()//2 - (max_cards_per_line / 2 - 0.5) * \
                (card_list[0].get_width() + card_spacing)

            topmost_centery = (self.get_height() - constants.DEFAULT_ROUND_BTN_HEIGHT)//2 - (max_cards_per_column / 2 - 0.5) * \
                (card_list[0].get_height() + card_spacing)

            for i, card in enumerate(card_list):
                line = i // max_cards_per_line
                card.set_center((leftmost_centerx + (i % max_cards_per_line) * (
                    card.get_width() + card_spacing), topmost_centery + line * (card.get_height() + card_spacing)))
