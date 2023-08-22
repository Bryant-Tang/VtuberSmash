from typing import List
from thread_management import ThreadManager
from gui_components import Scene, Component, Surface, Label, TextButton, MouseEventAdapter
from game_resource import image, constants
from network import CommunicateData, ClientRegistrant, ServerRegistrant
import pymsgbox

from .game import Game
from .battle_scene import BattleMode, BattleScene
from decorator import singleton


@singleton
class WaitConnectScene(Scene, ClientRegistrant, ServerRegistrant):
    _reserved_comp_list: List[Component]
    _prepared_btn: TextButton
    _is_waiting_connect: bool
    _is_prepared: bool

    def __init__(self) -> None:
        super().__init__(image.get_image(image.BG_BATTLE_FIELD),
                         (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self._reserved_comp_list = []
        self._is_waiting_connect = False
        self._is_prepared = False

        btn_spacing = 5

        self._back_btn = TextButton("返回")
        self._back_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: self._back()))
        self._back_btn.set_pos((self.get_width() - self._back_btn.get_width() * 2 - btn_spacing,
                                self.get_height() - self._back_btn.get_height()))
        self._reserved_comp_list.append(self._back_btn)

        def undo_prepare():
            self._is_prepared = False
            if Game().get_battle_mode() == BattleMode.SERVER:
                Game().get_server().send_undo_start_battle()
            elif Game().get_battle_mode() == BattleMode.CLIENT:
                Game().get_client().send_undo_start_battle()
            self.clear_component()
            for comp in self._reserved_comp_list:
                self.add_component(comp)
            self.add_component(self._prepared_btn)
        self._undo_prepared_btn = TextButton("取消準備")
        self._undo_prepared_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: undo_prepare()))
        self._undo_prepared_btn.set_pos((self.get_width() - self._undo_prepared_btn.get_width(),
                                         self.get_height() - self._undo_prepared_btn.get_height()))

        def start_battle():
            if ((Game().get_battle_mode() == BattleMode.SERVER) and (Game().get_server().is_connect())) or \
                    ((Game().get_battle_mode() == BattleMode.CLIENT) and (Game().get_client().is_connect())):
                self._is_prepared = True
                if Game().get_battle_mode() == BattleMode.SERVER:
                    Game().get_server().send_start_battle()
                elif Game().get_battle_mode() == BattleMode.CLIENT:
                    Game().get_client().send_start_battle()
                self.clear_component()
                self.add_component(self._undo_prepared_btn)
                ThreadManager().run_func_as_new_thread(target=self._waiting_start_thread_func)
        self._prepared_btn = TextButton("準備")
        self._prepared_btn.add_mouse_handler(
            MouseEventAdapter(mouse_click=lambda event: start_battle()))
        self._prepared_btn.set_pos((self.get_width() - self._prepared_btn.get_width(),
                                    self.get_height() - self._prepared_btn.get_height()))

    def _back(self):
        self.clear_component()
        self._is_waiting_connect = False
        self._is_prepared = False
        Game().get_server().close()
        Game().get_server().unregister(self)
        Game().get_client().close()
        Game().get_client().unregister(self)
        Game().remove_scene(self)

    def on_new_player_connected(self):
        Game().get_server().send_game_version(Game().get_version())
        return super().on_new_player_connected()

    def on_client_close(self):
        self.start_showing()

    def on_connect_to_server(self):
        return super().on_connect_to_server()

    def on_server_close(self):
        self._back()

    def _wait_server_game_version_thread_func(self):
        while (not Game().get_close_flag().is_set()) and (Game().get_battle_mode() == BattleMode.CLIENT):
            game_version_data = (Game().get_client().get_data(
                CommunicateData.GAME_VERSION))
            if game_version_data != None:
                server_game_version = game_version_data.data
                break
        print(f"server game version: {server_game_version}")
        if server_game_version != Game().get_version():
            pymsgbox.alert("與對方版本不同")
            self._back()

    def _waiting_start_thread_func(self):
        waiting_label = Label("等待對方準備...", constants.COLOR_WHITE)
        waiting_label_bg = Component(Surface(waiting_label.get_size()))
        self.add_component(waiting_label_bg)
        self.add_component(waiting_label)
        while (not Game().get_close_flag().is_set()) and ((Game().get_battle_mode() == BattleMode.SERVER) or (Game().get_battle_mode() == BattleMode.CLIENT)) and self._is_prepared:
            if ((Game().get_battle_mode() == BattleMode.SERVER) and (Game().get_server().get_data(CommunicateData.START_BATTLE))) or \
                    ((Game().get_battle_mode() == BattleMode.CLIENT) and (Game().get_client().get_data(CommunicateData.START_BATTLE))):
                break
        self.remove_component(waiting_label_bg)
        self.remove_component(waiting_label)
        if (not Game().get_close_flag().is_set()) and self._is_prepared:
            self.clear_component()
            Game().get_server().unregister(self)
            Game().get_client().unregister(self)
            Game().set_scene(BattleScene())

    def start_showing(self):
        ThreadManager().run_func_as_new_thread(target=self._waiting_connect_thread_func)

    def _waiting_connect_thread_func(self):
        if Game().get_battle_mode() == BattleMode.CLIENT:
            Game().get_client().register(self)
        elif Game().get_battle_mode() == BattleMode.SERVER:
            Game().get_server().register(self)
        self.clear_component()
        self._is_prepared = False
        self._is_waiting_connect = True
        for comp in self._reserved_comp_list:
            self.add_component(comp)
        if Game().get_battle_mode() == BattleMode.SERVER:
            waiting_label = Label("等待對方連線...", constants.COLOR_WHITE)
            waiting_label_bg = Component(Surface(waiting_label.get_size()))
            self.add_component(waiting_label_bg)
            self.add_component(waiting_label)
            while not Game().get_close_flag().is_set() and self._is_waiting_connect:
                if Game().get_server().is_connect():
                    break
            self.remove_component(waiting_label_bg)
            self.remove_component(waiting_label)
            if Game().get_server().is_connect():
                self.add_component(self._prepared_btn)
        elif Game().get_battle_mode() == BattleMode.CLIENT and Game().get_client().is_connect():
            self.add_component(self._prepared_btn)
            ThreadManager().run_func_as_new_thread(self._wait_server_game_version_thread_func)
        else:
            self._back()
