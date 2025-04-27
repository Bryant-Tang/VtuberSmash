from typing import List
import webbrowser
from gui_components import Scene, RoundButton, TextButton, MouseEventAdapter, Component, BaseButton
from game_resource import image, constants
from thread_management import ThreadManager
from decorator import singleton

from .game import Game


@singleton
class AboutGameScene(Scene):
    _page_list: List[Component]
    _current_page: int
    _btn_list: List[BaseButton]

    def __init__(self) -> None:
        super().__init__(image.get_image(image.BG_MENU),
                         (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self._page_list = []
        self._current_page = 0
        self._btn_list = []

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

        back_btn = TextButton("返回")
        back_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: Game().remove_scene(self)))
        back_btn.set_pos((self.get_width() - back_btn.get_width(),
                          self.get_height() - back_btn.get_height()))
        self.add_component(back_btn)
        self._btn_list.append(back_btn)

    def start_showing(self):
        ThreadManager().run_func_as_new_thread(target=self._show_announcement_thread_func)

    def _show_announcement_thread_func(self):
        self.clear_component()
        self._page_list = [Component(image.get_image(image.ABOUT_GAME_00)),
                           Component(image.get_image(image.ABOUT_GAME_01)),
                           Component(image.get_image(image.ABOUT_GAME_02)),
                           Component(image.get_image(image.ABOUT_GAME_03)),]
        self._turn_to_page(0)

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
        self.add_component(self._page_list[self._current_page], 0)
        if self._current_page == 0:
            self._show_go_to_source_web_site_btn()

    def _show_go_to_source_web_site_btn(self):
        def go_to_source_web_site():
            webbrowser.open(
                "https://docs.google.com/spreadsheets/d/1fFsrIthL3hRCmAfEwJMlgfG2_bWhB1u9jkBZxz0r6QU/edit?usp=sharing")
        btn = TextButton("前往連結")
        btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: go_to_source_web_site()))
        btn.set_pos((self.get_width() - 600,
                     100))
        self.add_component(btn)
