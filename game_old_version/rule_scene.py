from typing import Callable, List
from gui_components import Scene, TextButton, MouseEventAdapter, Component, RoundButton
import source

from .decorator import singleton


@singleton
class RuleScene(Scene):
    _page_list: List[Component]
    _current_page_index: int

    def __init__(self) -> None:
        super().__init__(source.image.get_image(source.image.BG_MENU),
                         (source.constants.WINDOW_WIDTH, source.constants.WINDOW_HEIGHT))
        self._page_list = [Component(source.image.get_image(source.image.GAME_RULE_0)),
                           Component(source.image.get_image(source.image.GAME_RULE_1)),
                           Component(source.image.get_image(source.image.GAME_RULE_2))]
        self._current_page_index = 0
        self.add_component(self._page_list[self._current_page_index], 0)

    def init(self, back_to_menu: Callable[[], None]):
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

        start_btn = TextButton("返回")
        start_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: back_to_menu()))
        start_btn.set_pos((self.get_width() - start_btn.get_width(),
                           self.get_height() - start_btn.get_height()))
        self.add_component(start_btn)

    def _go_left_page(self) -> None:
        self.remove_component(self._page_list[self._current_page_index])
        self._current_page_index = max(0, self._current_page_index - 1)
        self.add_component(self._page_list[self._current_page_index], 0)

    def _go_right_page(self) -> None:
        self.remove_component(self._page_list[self._current_page_index])
        self._current_page_index = min(
            len(self._page_list) - 1, self._current_page_index + 1)
        self.add_component(self._page_list[self._current_page_index], 0)
