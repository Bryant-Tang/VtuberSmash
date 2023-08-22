from thread_management import ThreadManager
from typing import List
from gui_components import Scene, RoundButton, TextButton, MouseEventAdapter, Component, BaseButton, Box, Surface, Label
from game_resource import image, constants
from game_element import player_factory
from decorator import singleton

from .game import Game


@singleton
class EditPlayerScene(Scene):
    _page_list: List[Component]
    _current_page: int
    _selected_player_id: int
    _btn_list: List[BaseButton]
    _lock_sign: Box

    def __init__(self) -> None:
        super().__init__(image.get_image(image.BG_MENU),
                         (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self._page_list = []
        self._current_page = 0
        self._btn_list = []
        self._selected_player_id = None
        self._lock_sign = Box(Surface(self.get_size()))
        self._lock_sign.set_alpha(constants.CARD_MASK_ALPHA)
        self._lock_sign.fill(constants.COLOR_GRAY)
        lock_comp = Component(image.get_image(image.CARD_LOCK))
        lock_comp.set_center(
            (self._lock_sign.get_width()//2, self._lock_sign.get_height()//2))
        self._lock_sign.add_component(lock_comp)

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

        def back_to_menu_with_setting_player_id():
            Game().set_player_id(self._selected_player_id)
            Game().remove_scene(self)
        confirm_btn = TextButton("確定")
        confirm_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: back_to_menu_with_setting_player_id()))
        confirm_btn.set_pos((self.get_width() - confirm_btn.get_width(),
                             self.get_height() - confirm_btn.get_height()))
        self.add_component(confirm_btn)
        self._btn_list.append(confirm_btn)

    def start_showing(self):
        ThreadManager().run_func_as_new_thread(
            target=self._show_all_player_detail_thread_func)

    def _show_all_player_detail_thread_func(self):
        self.clear_component()
        self._page_list = [player_factory.get_player_detail(
            player_id) for player_id in player_factory.get_all_player_id()]
        self._selected_player_id = Game().get_player_id()
        self._turn_to_page(self._selected_player_id)

    def _go_left_page(self) -> None:
        if self._current_page > 0:
            self._turn_to_page(self._current_page - 1)

    def _go_right_page(self) -> None:
        if self._current_page < len(self._page_list) - 1:
            self._turn_to_page(self._current_page + 1)

    def _turn_to_page(self, page: int) -> None:
        self.clear_component()
        self._current_page = page
        self.add_component(self._page_list[self._current_page], 0)
        player_creating_information = Game().get_player_creating_information(self._current_page)
        hp_label = Label(
            f"{player_creating_information.hp}/{player_creating_information.max_hp}")
        hp_label.set_pos((726, 155))
        self.add_component(hp_label)
        shield_label = Label(
            f"{player_creating_information.shield}/{player_creating_information.max_shield}")
        shield_label.set_pos((726, 215))
        self.add_component(shield_label)
        if page in Game().get_unlock_player_id_list():
            self._selected_player_id = page
            self.remove_component(self._lock_sign)
        elif self.get_component_index(self._lock_sign) == None:
            self.add_component(self._lock_sign)
        for btn in self._btn_list:
            self.add_component(btn)
