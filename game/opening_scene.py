from thread_management import ThreadManager
from typing import Callable
from gui_components import Scene
from game_resource import image, constants
from decorator import singleton

from .game import Game
from .delay import delay
from .menu_scene import MenuScene


@singleton
class OpeningScene(Scene):
    _go_to_menu_scene_with_show_player_fullbody: Callable[[], None]

    def __init__(self) -> None:
        super().__init__(image.get_image(image.DECLARATION_ZH),
                         (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self._go_to_menu_scene_with_show_player_fullbody = None


    def start_showing(self):
        ThreadManager().run_func_as_new_thread(target=self._show_opening_thread_func)

    def _show_opening_thread_func(self):
        self.clear_component()
        Game().pause_bgm(0)
        delay(3000)
        self.set_background(image.get_image(image.DECLARATION_EN))
        delay(3000)
        Game().resume_bgm(0)
        Game().remove_scene(self)
        Game().set_scene(MenuScene())
