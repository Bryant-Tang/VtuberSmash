from thread_management import ThreadManager
from typing import List
from gui_components import Scene, Component, TextButton, MouseEventAdapter, Label
from game_resource import image, constants
from game_element import player_factory, card_factory
from pygame import mouse as pygame_mouse
from decorator import singleton
import pymsgbox
from network import is_valid_ip, is_valid_port

from .game import Game
from .battle_scene import BattleMode, BattleScene
from .wait_connect_scene import WaitConnectScene
from .edit_deck_scene import EditDeckScene
from .edit_player_scene import EditPlayerScene
from .delay import delay


@singleton
class ChooseModeScene(Scene):
    _reserved_comp_list: List[Component]
    _player_fullbody: Component
    _detail: Component
    _easy_mode_btn: TextButton
    _normal_mode_btn: TextButton
    _hard_mode_btn: TextButton
    _super_hard_mode_btn: TextButton
    _asian_mode_btn: TextButton
    _random_mode_btn: TextButton
    _create_connect_btn: TextButton
    _join_connect_btn: TextButton

    def __init__(self) -> None:
        super().__init__(image.get_image(image.BG_MENU),
                         (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self._reserved_comp_list = []
        self._player_fullbody = None
        self._detail = None

        btn_spacing = 5

        # 第一列
        def start_easy_battle():
            Game().set_battle_mode(BattleMode.EASY)
            Game().set_scene(BattleScene())
        self._easy_mode_btn = TextButton("簡單")
        self._easy_mode_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: start_easy_battle()))
        self._easy_mode_btn.set_x(697)
        self._easy_mode_btn.set_y(self.get_height()//2 - 10 -
                                  int((self._easy_mode_btn.get_height() + btn_spacing) * 5/2))
        self.add_component(self._easy_mode_btn)
        self._reserved_comp_list.append(self._easy_mode_btn)

        def start_normal_battle():
            Game().set_battle_mode(BattleMode.NORMAL)
            Game().set_scene(BattleScene())
        self._normal_mode_btn = TextButton("普通")
        self._normal_mode_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: start_normal_battle()))
        self._normal_mode_btn.set_x(self._easy_mode_btn.get_x())
        self._normal_mode_btn.set_y(
            self._easy_mode_btn.get_bottom() + btn_spacing)
        self.add_component(self._normal_mode_btn)
        self._reserved_comp_list.append(self._normal_mode_btn)

        def start_hard_battle():
            Game().set_battle_mode(BattleMode.HARD)
            Game().set_scene(BattleScene())
        self._hard_mode_btn = TextButton("困難")
        self._hard_mode_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: start_hard_battle()))
        self._hard_mode_btn.set_x(self._easy_mode_btn.get_x())
        self._hard_mode_btn.set_y(
            self._normal_mode_btn.get_bottom() + btn_spacing)
        self.add_component(self._hard_mode_btn)
        self._reserved_comp_list.append(self._hard_mode_btn)

        def start_super_hard_battle():
            Game().set_battle_mode(BattleMode.SUPER_HARD)
            Game().set_scene(BattleScene())
        self._super_hard_mode_btn = TextButton("超級難")
        self._super_hard_mode_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: start_super_hard_battle()))
        self._super_hard_mode_btn.set_x(self._easy_mode_btn.get_x())
        self._super_hard_mode_btn.set_y(
            self._hard_mode_btn.get_bottom() + btn_spacing)
        self.add_component(self._super_hard_mode_btn)
        self._reserved_comp_list.append(self._super_hard_mode_btn)

        def start_asian_battle():
            Game().set_battle_mode(BattleMode.ASIAN)
            Game().set_scene(BattleScene())
        self._asian_mode_btn = TextButton("亞洲人")
        self._asian_mode_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: start_asian_battle()))
        self._asian_mode_btn.set_x(self._easy_mode_btn.get_x())
        self._asian_mode_btn.set_y(
            self._super_hard_mode_btn.get_bottom() + btn_spacing)
        self.add_component(self._asian_mode_btn)
        self._reserved_comp_list.append(self._asian_mode_btn)

        # 第二列
        def start_random_battle():
            Game().set_battle_mode(BattleMode.RANDOM)
            Game().set_scene(BattleScene())
        self._random_mode_btn = TextButton("隨機")
        self._random_mode_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: start_random_battle()))
        self._random_mode_btn.set_x(903)
        self._random_mode_btn.set_y(self.get_height()//2 - 10 -
                                    int((self._random_mode_btn.get_height() + btn_spacing) * 5/2))
        self.add_component(self._random_mode_btn)
        self._reserved_comp_list.append(self._random_mode_btn)

        def start_server_battle():
            host = pymsgbox.prompt(text="請輸入要建立的Server IP (請用英文輸入法才能打\".\")")
            if host == None:
                return
            if not is_valid_ip(host):
                pymsgbox.alert("請輸入正確的IP")
                return
            port = pymsgbox.prompt(
                text="請輸入要建立的Server port (1024 ~ 49151)", default="35235")
            if port == None:
                return
            if not is_valid_port(port):
                pymsgbox.alert("請輸入正確的Port")
                return
            Game().get_server().open()
            ThreadManager().run_func_as_new_thread(
                    target=Game().get_server().start_search_client, args=[host, int(port)])
            Game().set_battle_mode(BattleMode.SERVER)
            Game().set_scene(WaitConnectScene())
        self._create_connect_btn = TextButton("創建房間")
        self._create_connect_btn.add_mouse_handler(
            MouseEventAdapter(
                mouse_click=lambda event: start_server_battle()))
        self._create_connect_btn.set_x(self._random_mode_btn.get_x())
        self._create_connect_btn.set_y(
            self._random_mode_btn.get_bottom() + btn_spacing)
        self.add_component(self._create_connect_btn)
        self._reserved_comp_list.append(self._create_connect_btn)

        def start_client_battle():
            host = pymsgbox.prompt(text="請輸入要連線的Server IP (請用英文輸入法才能打\".\")")
            if host == None:
                return
            if not is_valid_ip(host):
                pymsgbox.alert("請輸入正確的IP")
                return
            port = pymsgbox.prompt(
                text="請輸入要連線的Server port (1024 ~ 49151)", default="35235")
            if port == None:
                return
            if not is_valid_port(port):
                pymsgbox.alert("請輸入正確的Port")
                return
            Game().get_client().open()
            connect_result = Game().get_client().connect_to_server(host, int(port))
            if connect_result:
                Game().set_battle_mode(BattleMode.CLIENT)
                Game().set_scene(WaitConnectScene())
            else:
                pymsgbox.alert("連線失敗", "connect fail")
                Game().get_client().close()
        self._join_connect_btn = TextButton("加入房間")
        self._join_connect_btn.add_mouse_handler(
            MouseEventAdapter(
                mouse_click=lambda event: start_client_battle()))
        self._join_connect_btn.set_x(self._create_connect_btn.get_x())
        self._join_connect_btn.set_y(
            self._create_connect_btn.get_bottom() + btn_spacing)
        self.add_component(self._join_connect_btn)
        self._reserved_comp_list.append(self._join_connect_btn)

        edit_player_btn = TextButton("選擇角色")
        edit_player_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: Game().set_scene(EditPlayerScene())))
        edit_player_btn.set_x(self._create_connect_btn.get_x())
        edit_player_btn.set_y(
            self._join_connect_btn.get_bottom() + btn_spacing)
        self.add_component(edit_player_btn)
        self._reserved_comp_list.append(edit_player_btn)

        edit_deck_btn = TextButton("編輯牌組")
        edit_deck_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: Game().set_scene(EditDeckScene())))
        edit_deck_btn.set_x(self._create_connect_btn.get_x())
        edit_deck_btn.set_y(edit_player_btn.get_bottom() + btn_spacing)
        self.add_component(edit_deck_btn)
        self._reserved_comp_list.append(edit_deck_btn)

        back_btn = TextButton("返回")
        back_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: Game().remove_scene(self)))
        back_btn.set_pos((self.get_width() - back_btn.get_width(),
                          self.get_height() - back_btn.get_height()))
        self.add_component(back_btn)
        self._reserved_comp_list.append(back_btn)

        self.add_mouse_handler(MouseEventAdapter(
            any_event=lambda event: self._handle_mouse_move()))

    def start_showing(self):
        ThreadManager().run_func_as_new_thread(
            target=self._show_player_and_deck_thread_func)

    def _show_player_and_deck_thread_func(self):
        self.clear_component()
        if self._player_fullbody:
            self.remove_component(self._player_fullbody)
        self._player_fullbody \
            = player_factory.get_player_fullbody_comp(Game().get_player_id())
        self.add_component(self._player_fullbody)

        player_creating_information = Game(
        ).get_player_creating_information(Game().get_player_id())
        hp_label = Label(
            f"血量: {player_creating_information.hp}/{player_creating_information.max_hp}")
        hp_label.set_pos((0, 0))
        self.add_component(hp_label)
        shield_label = Label(
            f"護盾: {player_creating_information.shield}/{player_creating_information.max_shield}")
        shield_label.set_pos((0, 50))
        self.add_component(shield_label)

        deck = [card_factory.get_card(card_id)
                for card_id in Game().get_player_card_id_list()]
        card_x = 0
        row = 0
        for card in deck:
            card.set_x(card_x)
            card_x += 55
            card.set_y(270 + row * 130)
            if card_x >= 550:
                row += 1
                card_x = 0
            self.add_component(card)
        for comp in self._reserved_comp_list:
            self.add_component(comp)

        delay(100)
        self._handle_mouse_move()

    def _set_detail(self, comp: Component):
        self.remove_component(self._detail)
        self._detail = comp
        self.add_component(self._detail)

    def _remove_detail(self):
        self.remove_component(self._detail)
        self._detail = None

    def _handle_mouse_move(self):
        mouse_pos = pygame_mouse.get_pos()
        if self._easy_mode_btn.is_collide(mouse_pos):
            self._set_detail(
                Component(image.get_image(image.MODE_DETAIL_EASY)))
        elif self._normal_mode_btn.is_collide(mouse_pos):
            self._set_detail(
                Component(image.get_image(image.MODE_DETAIL_NORMAL)))
        elif self._hard_mode_btn.is_collide(mouse_pos):
            self._set_detail(
                Component(image.get_image(image.MODE_DETAIL_HARD)))
        elif self._super_hard_mode_btn.is_collide(mouse_pos):
            self._set_detail(
                Component(image.get_image(image.MODE_DETAIL_SUPER_HARD)))
        elif self._asian_mode_btn.is_collide(mouse_pos):
            self._set_detail(
                Component(image.get_image(image.MODE_DETAIL_ASIAN)))
        elif self._random_mode_btn.is_collide(mouse_pos):
            self._set_detail(
                Component(image.get_image(image.MODE_DETAIL_RANDOM)))
        elif self._create_connect_btn.is_collide(mouse_pos):
            self._set_detail(Component(image.get_image(
                image.MODE_DETAIL_CREATE_CONNECT)))
        elif self._join_connect_btn.is_collide(mouse_pos):
            self._set_detail(
                Component(image.get_image(image.MODE_DETAIL_JOIN_CONNECT)))
        else:
            self._remove_detail()
