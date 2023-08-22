from abc import abstractmethod
from typing import Callable
import pygame

from .component import Event


class MouseEventHandler:
    _is_down: bool

    def __init__(self) -> None:
        self._is_down = None

    def handle_event(self, event: Event, is_collide: bool):
        self.any_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and is_collide:
            self._is_down = True
            self.mouse_down(event)
        elif event.type == pygame.MOUSEBUTTONUP and self._is_down == True and is_collide:
            self.mouse_up(event)
            self.mouse_click(event)
            self._is_down = False
        elif not is_collide:
            self._is_down = False

    @abstractmethod
    def mouse_up(self, event: Event):
        pass

    @abstractmethod
    def mouse_down(self, event: Event):
        pass

    @abstractmethod
    def mouse_click(self, event: Event):
        pass

    @abstractmethod
    def any_event(self, event: Event):
        pass


class MouseEventAdapter(MouseEventHandler):

    def __init__(self, mouse_up: Callable[[Event], None] = None,
                 mouse_down: Callable[[Event], None] = None,
                 mouse_click: Callable[[Event], None] = None,
                 any_event: Callable[[Event], None] = None) -> None:
        super().__init__()
        self._mouse_up_implement = mouse_up
        self._mouse_down_implement = mouse_down
        self._mouse_click_implement = mouse_click
        self._any_event_implement = any_event

    def mouse_up(self, event: Event):
        if self._mouse_up_implement:
            self._mouse_up_implement(event)

    def mouse_down(self, event: Event):
        if self._mouse_down_implement:
            self._mouse_down_implement(event)

    def mouse_click(self, event: Event):
        if self._mouse_click_implement:
            self._mouse_click_implement(event)

    def any_event(self, event: Event):
        if self._any_event_implement:
            self._any_event_implement(event)
