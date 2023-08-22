from typing import Callable
from gui_components import Scene, TextButton, MouseEventAdapter
import source

from .decorator import singleton


@singleton
class MenuScene(Scene):
    def __init__(self) -> None:
        super().__init__(source.image.get_image(source.image.BG_MENU),
                         (source.constants.WINDOW_WIDTH, source.constants.WINDOW_HEIGHT))

    def init(self, start_battle: Callable[[], None], read_rule: Callable[[], None], edit_card: Callable[[], None], edit_player: Callable[[], None]):
        btn_spacing = 5
        start_btn = TextButton("開始")
        start_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: start_battle()))
        start_btn.set_center(
            (self.get_width()//2, start_btn.get_centery()))
        start_btn.set_y(self.get_height()//2 - start_btn.get_height() * 2)
        self.add_component(start_btn)

        read_rule_btn = TextButton("閱讀規則")
        read_rule_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: read_rule()))
        read_rule_btn.set_center(
            (self.get_width()//2, read_rule_btn.get_centery()))
        read_rule_btn.set_y(start_btn.get_bottom() + btn_spacing)
        self.add_component(read_rule_btn)

        edit_card_btn = TextButton("編輯牌組")
        edit_card_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: edit_card()))
        edit_card_btn.set_center(
            (self.get_width()//2, edit_card_btn.get_centery()))
        edit_card_btn.set_y(read_rule_btn.get_bottom() + btn_spacing)
        self.add_component(edit_card_btn)

        edit_player_btn = TextButton("選擇角色")
        edit_player_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: edit_player()))
        edit_player_btn.set_center(
            (self.get_width()//2, edit_player_btn.get_centery()))
        edit_player_btn.set_y(edit_card_btn.get_bottom() + btn_spacing)
        self.add_component(edit_player_btn)
