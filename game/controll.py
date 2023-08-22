from .init_pygame import init as pygame_init
from game_element import init as game_element_init
from .game import Game
from .opening_scene import OpeningScene


def init():
    pygame_init()
    game_element_init()


def start_game():
    init()
    Game().set_scene(OpeningScene())
    Game().start_gui_loop()
