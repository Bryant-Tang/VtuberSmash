from thread_management import ThreadManager
from typing import List
from gui_components import Scene, TextButton, MouseEventAdapter, Component, Label, Surface
from game_resource import image, constants
from game_element import player_factory
from decorator import singleton

from .game import Game
from .read_rule_scene import ReadRuleScene
from .edit_deck_scene import EditDeckScene
from .edit_player_scene import EditPlayerScene
from .about_game_scene import AboutGameScene
from .card_handbook_scene import CardHandbookScene
from .player_effect_handbook_scene import PlayerEffectHandbookScene
from .gacha_scene import GachaScene
from .choose_mode_scene import ChooseModeScene


@singleton
class MenuScene(Scene):
    _player_fullbody: Component
    _reserved_comp_list: List[Component]

    def __init__(self) -> None:
        super().__init__(image.get_image(image.BG_MENU),
                         (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self._player_fullbody = None
        self._reserved_comp_list = []

        btn_spacing = 5

        start_btn = TextButton("開始戰鬥")
        start_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: Game().set_scene(ChooseModeScene())))
        start_btn.set_width(constants.DEFAULT_TEXT_BTN_WIDTH * 2 + btn_spacing)
        start_btn.set_background_pair(image.get_image(
            image.BTN_TEXT_UP_WIDTH2X), image.get_image(image.BTN_TEXT_DOWN_WIDTH2X))
        start_btn.set_center((900, 0))
        start_btn.set_y(self.get_height()//2 -
                        int((start_btn.get_height() + btn_spacing) * 5/2))
        self.add_component(start_btn)
        self._reserved_comp_list.append(start_btn)

        # 第一列
        edit_player_btn = TextButton("選擇角色")
        edit_player_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: Game().set_scene(EditPlayerScene())))
        edit_player_btn.set_x(start_btn.get_x())
        edit_player_btn.set_y(start_btn.get_bottom() + btn_spacing)
        self.add_component(edit_player_btn)
        self._reserved_comp_list.append(edit_player_btn)

        edit_deck_btn = TextButton("編輯牌組")
        edit_deck_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: Game().set_scene(EditDeckScene())))
        edit_deck_btn.set_x(start_btn.get_x())
        edit_deck_btn.set_y(edit_player_btn.get_bottom() + btn_spacing)
        self.add_component(edit_deck_btn)
        self._reserved_comp_list.append(edit_deck_btn)

        gacha_btn = TextButton("再一單")
        gacha_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: Game().set_scene(GachaScene())))
        gacha_btn.set_x(start_btn.get_x())
        gacha_btn.set_y(edit_deck_btn.get_bottom() + btn_spacing)
        self.add_component(gacha_btn)
        self._reserved_comp_list.append(gacha_btn)

        about_game_btn = TextButton("其他告示")
        about_game_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: Game().set_scene(AboutGameScene())))
        about_game_btn.set_x(start_btn.get_x())
        about_game_btn.set_y(gacha_btn.get_bottom() + btn_spacing)
        self.add_component(about_game_btn)
        self._reserved_comp_list.append(about_game_btn)

        # 第二列
        read_rule_btn = TextButton("閱讀規則")
        read_rule_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: Game().set_scene(ReadRuleScene())))
        read_rule_btn.set_x(edit_player_btn.get_right() + btn_spacing)
        read_rule_btn.set_y(start_btn.get_bottom() + btn_spacing)
        self.add_component(read_rule_btn)
        self._reserved_comp_list.append(read_rule_btn)

        card_handbook_btn = TextButton("卡牌圖鑑")
        card_handbook_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: Game().set_scene(CardHandbookScene())))
        card_handbook_btn.set_x(edit_player_btn.get_right() + btn_spacing)
        card_handbook_btn.set_y(read_rule_btn.get_bottom() + btn_spacing)
        self.add_component(card_handbook_btn)
        self._reserved_comp_list.append(card_handbook_btn)

        player_effect_handbook_btn = TextButton("角色效果")
        player_effect_handbook_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: Game().set_scene(PlayerEffectHandbookScene())))
        player_effect_handbook_btn.set_x(
            edit_player_btn.get_right() + btn_spacing)
        player_effect_handbook_btn.set_y(
            card_handbook_btn.get_bottom() + btn_spacing)
        self.add_component(player_effect_handbook_btn)
        self._reserved_comp_list.append(player_effect_handbook_btn)

        version_label = Label(
            f"version:{Game().get_version()}", constants.COLOR_BLACK, 18)
        version_label.set_x(0)
        version_label.set_y(self.get_height() - version_label.get_height())
        self.add_component(version_label)
        self._reserved_comp_list.append(version_label)

    def start_showing(self):
        ThreadManager().run_func_as_new_thread(
            target=self._show_player_fullbody_thread_func)

    def _show_user_point(self):
        user_point_label = Label(
            f"Pt: {Game().get_user_point()}", constants.COLOR_WHITE)
        user_point_label_bg = Component(Surface(user_point_label.get_size()))
        self.add_component(user_point_label_bg)
        self.add_component(user_point_label)

    def _show_player_fullbody_thread_func(self):
        self.clear_component()
        if self._player_fullbody:
            self.remove_component(self._player_fullbody)
        self._player_fullbody \
            = player_factory.get_player_fullbody_comp(Game().get_player_id())
        self.add_component(self._player_fullbody)
        self._show_user_point()
        for comp in self._reserved_comp_list:
            self.add_component(comp)
