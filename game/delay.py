from pygame import time as pygame_time

from .game import Game


def delay(milliseconds: int):
    start_time = pygame_time.get_ticks()
    while not Game().get_close_flag().is_set():
        current_time = pygame_time.get_ticks()
        elapsed_time = current_time - start_time

        if elapsed_time >= milliseconds:
            break
