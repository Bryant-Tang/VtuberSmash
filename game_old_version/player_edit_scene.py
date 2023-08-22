from typing import Callable, List
from gui_components import Scene, RoundButton, TextButton, MouseEventAdapter, Component, BaseButton
import source

from .player import Player
from .decorator import singleton

_get_all_player: Callable[[], List[Component]]
_get_current_player: Callable[[], Player]


def init(get_all_player: Callable[[], List[Component]], get_current_player: Callable[[], Player]):
    global _get_all_player
    global _get_current_player
    _get_all_player = get_all_player
    _get_current_player = get_current_player


@singleton
class PlayerEditScene(Scene):
    _selected_player: Player
    _showing_player_index: int
    _all_player_detail_list: List[Component]
    _btn_list: List[BaseButton]

    def __init__(self) -> None:
        super().__init__(source.image.get_image(source.image.BG_MENU),
                         (source.constants.WINDOW_WIDTH, source.constants.WINDOW_HEIGHT))
        self._selected_player = None
        self._showing_player_index = 0
        self._all_player_detail_list = []
        self._btn_list = []

    def init(self, back_to_menu_with_setting_player: Callable[[int], None]):
        left_btn = RoundButton(source.image.get_image(source.image.BTN_LEFT_UP),
                               source.image.get_image(source.image.BTN_LEFT_DOWN))
        left_btn.set_x(self.get_centerx() - left_btn.get_width() - 10)
        left_btn.set_y(self.get_height() - left_btn.get_height())
        left_btn.add_mouse_handler(MouseEventAdapter(
            mouse_click=lambda event: self._go_left_page()))
        right_btn = RoundButton(source.image.get_image(source.image.BTN_RIGHT_UP),
                                source.image.get_image(source.image.BTN_RIGHT_DOWN))
        right_btn.set_x(self.get_centerx() + 10)
        right_btn.set_y(self.get_height() - right_btn.get_height())
        right_btn.add_mouse_handler(MouseEventAdapter(
            mouse_click=lambda event: self._go_right_page()))
        self.add_component(left_btn)
        self.add_component(right_btn)
        self._btn_list.append(left_btn)
        self._btn_list.append(right_btn)

        confirm_btn = TextButton("確定")
        confirm_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: back_to_menu_with_setting_player(self._showing_player_index)))
        confirm_btn.set_pos((self.get_width() - confirm_btn.get_width(),
                             self.get_height() - confirm_btn.get_height()))
        self.add_component(confirm_btn)
        self._btn_list.append(confirm_btn)

    def _go_left_page(self) -> None:
        if self._showing_player_index > 0:
            self.remove_component(
                self._all_player_detail_list[self._showing_player_index])
            self._showing_player_index -= 1
            self.add_component(
                self._all_player_detail_list[self._showing_player_index], 0)

    def _go_right_page(self) -> None:
        if self._showing_player_index < len(self._all_player_detail_list) - 1:
            self.remove_component(
                self._all_player_detail_list[self._showing_player_index])
            self._showing_player_index += 1
            self.add_component(
                self._all_player_detail_list[self._showing_player_index], 0)

    def show_player(self):
        self._all_player_detail_list = _get_all_player()
        self._selected_player = _get_current_player()
        self._showing_player_index = self._selected_player.get_id()
        self.clear_component()
        for btn in self._btn_list:
            self.add_component(btn)
        self.add_component(
            self._all_player_detail_list[self._showing_player_index], 0)
