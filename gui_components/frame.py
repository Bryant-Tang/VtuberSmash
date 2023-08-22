import os
import sys
from threading import Thread, Event as ThreadEvent
import threading
from typing import List, Tuple
from pygame import display as pygame_display, event as pygame_event, QUIT as pygame_QUIT, quit as pygame_quit, time as pygame_time, mixer as pygame_mixer
from pygame.mixer import Channel, Sound
from thread_management import ThreadManager
from game_resource import constants, font

from .scene import Scene, Surface


class Frame:
    _window: Surface
    _scenes: List[Scene]
    _active_scene: Scene
    _bgm_channel: Channel
    _bgm_channel_volume: float
    _is_bgm_pause: bool
    _bgm_list: List[Sound]
    _close_flag: threading.Event

    def __init__(self, size: Tuple[int, int], bgm_list: List[Sound] = None) -> None:
        self._window = pygame_display.set_mode(size)
        self._scenes = []
        self._active_scene = None
        self._bgm_channel = pygame_mixer.find_channel()
        self._bgm_channel_volume = self._bgm_channel.get_volume()
        self._is_bgm_pause = False
        self._bgm_list = []
        self._close_flag = threading.Event()
        if bgm_list:
            self._bgm_list.extend(bgm_list)

    def get_close_flag(self):
        return self._close_flag

    def set_scene(self, scene: Scene) -> None:
        if scene not in self._scenes:
            self._scenes.append(scene)
        self._active_scene = scene
        self._active_scene.start_showing()

    def remove_scene(self, scene: Scene) -> None:
        if scene in self._scenes:
            self._scenes.remove(scene)
            if len(self._scenes) != 0:
                self._active_scene = self._scenes[-1]
                self._active_scene.start_showing()

    def _handle_input(self) -> None:
        for event in pygame_event.get():
            if event.type == pygame_QUIT:
                self._close_flag.set()
            if self._active_scene:
                self._active_scene.handle_input(event)

    def set_bgm_list(self, bgm_list: List[Sound]):
        self._bgm_list = [bgm for bgm in bgm_list]
        self._change_playing_bgm()

    def _change_playing_bgm(self):
        current_bgm = self._bgm_channel.get_sound()
        if len(self._bgm_list) == 0:
            self._bgm_channel.stop()
            return
        if current_bgm not in self._bgm_list and len(self._bgm_list) > 0:
            self._bgm_channel.fadeout(constants.CHANGE_BGM_LATE)
            bgm = self._bgm_list.pop(0)
            self._bgm_channel.play(bgm)
            self._bgm_channel_volume = self._bgm_channel.get_volume()
            self._bgm_list.append(bgm)

    def pause_bgm(self, fade_out: int):
        ThreadManager().run_func_as_new_thread(
            target=self._pause_bgm, args=[fade_out])

    def _pause_bgm(self, fade_out: int):
        self._is_bgm_pause = True
        self.adjust_bgm_volume_gradually(end_volume=0, duration=fade_out)
        self._bgm_channel.pause()

    def resume_bgm(self, fade_in: int):
        ThreadManager().run_func_as_new_thread(
            target=self._resume_bgm, args=[fade_in])

    def _resume_bgm(self, fade_in: int):
        self._bgm_channel.set_volume(0)
        self._bgm_channel.unpause()
        self.adjust_bgm_volume_gradually(
            end_volume=self._bgm_channel_volume, duration=fade_in)
        self._is_bgm_pause = False

    def adjust_bgm_volume_gradually(self, end_volume: float, duration: int):
        start_time = pygame_time.get_ticks()
        start_volume = self._bgm_channel.get_volume()
        while True:
            current_time = pygame_time.get_ticks()
            elapsed_time = current_time - start_time
            if (elapsed_time >= duration) or (not self.is_running()):
                self._bgm_channel.set_volume(end_volume)
                break
            self._bgm_channel.set_volume(
                start_volume + (elapsed_time/duration)*(end_volume - start_volume))

    def paint(self) -> None:
        if self._active_scene:
            self._active_scene.paint(self._window, (0, 0))
        pygame_display.update()

    def is_running(self) -> bool:
        return not self._close_flag.is_set()

    def _close(self):
        self._window.fill(constants.COLOR_BLACK)
        self._window.blit(
            font.get_font(font.DEFAULT, constants.DEFAULT_FONT_SIZE).render("closing...", True, constants.COLOR_WHITE), (0, 0))
        self._window.blit(
            font.get_font(font.DEFAULT, constants.DEFAULT_FONT_SIZE).render("註: 如果關閉時卡在這個畫面，請使用工作管理員強制關閉。", True, constants.COLOR_WHITE), (0, 50))
        pygame_display.update()
        while True:
            if ThreadManager().is_all_thread_end():
                break
        while pygame_mixer.get_busy():
            pygame_mixer.stop()
        if os.path.exists("force_end_delay.txt"):
            pygame_time.delay(100)

    def _gui_loop(self):
        self._running = True
        while self.is_running():
            self._handle_input()
            self.paint()
            if (not self._is_bgm_pause) and (not self._bgm_channel.get_busy()):
                self._change_playing_bgm()
        self._close()
        pygame_quit()
        sys.exit()

    def start_gui_loop(self):
        Thread(target=self._gui_loop()).start()
