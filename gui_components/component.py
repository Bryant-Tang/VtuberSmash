from typing import List, Tuple, Union
from pygame import Surface, Rect, Color, transform as pygame_transform, mouse as pygame_mouse
from pygame.event import Event

from .mouse_event_handler import MouseEventHandler


class Component:
    _surface: Surface
    _collision_rect: Rect
    _mouse_handlers: List[MouseEventHandler]
    _visible: bool
    _auto_scale: bool

    def __init__(self, background: Surface, rect: Rect = None) -> None:
        self._surface = background
        self._collision_rect = self._surface.get_rect()
        self._mouse_handlers = []
        self._self_trigger_event_handlers = []
        self._visible = True
        self._auto_scale = True
        self._rotate_angle = 0
        if rect == None:
            self._collision_rect = self._surface.get_rect()
        else:
            self._collision_rect = rect.copy()

    def set_x(self, x: int) -> None:
        self._collision_rect.x = x

    def set_y(self, y: int) -> None:
        self._collision_rect.y = y

    def set_pos(self, x_y: Tuple[int, int]) -> None:
        self.set_x(x_y[0])
        self.set_y(x_y[1])

    def set_center(self, x_y: Tuple[int, int]) -> None:
        self._collision_rect.center = x_y

    def set_width(self, width: int) -> None:
        self._collision_rect.width = width

    def set_height(self, height: int) -> None:
        self._collision_rect.height = height

    def set_size(self, size: Tuple[int, int]) -> None:
        self.set_width(size[0])
        self.set_height(size[1])

    def set_rect(self, rect: Rect) -> None:
        self.set_pos(rect.topleft)
        self.set_size(rect.size)

    def get_x(self) -> int:
        return self._collision_rect.x

    def get_y(self) -> int:
        return self._collision_rect.y

    def get_pos(self) -> Tuple[int, int]:
        return self._collision_rect.topleft

    def get_left(self) -> int:
        return self._collision_rect.left

    def get_right(self) -> int:
        return self._collision_rect.right

    def get_top(self) -> int:
        return self._collision_rect.top

    def get_bottom(self) -> int:
        return self._collision_rect.bottom

    def get_centerx(self) -> int:
        return self._collision_rect.centerx

    def get_centery(self) -> int:
        return self._collision_rect.centery

    def get_center(self) -> Tuple[int, int]:
        return self._collision_rect.center

    def get_width(self) -> int:
        return self._collision_rect.width

    def get_height(self) -> int:
        return self._collision_rect.height

    def get_size(self) -> Tuple[int, int]:
        return self._collision_rect.size

    def get_rect(self) -> Rect:
        return self._collision_rect.copy()

    def get_background(self) -> Surface:
        return self._surface.copy()

    def set_background(self, background: Surface) -> None:
        if background:
            new_surface_rect = background.get_rect()
            if self._auto_scale and (self.get_width() != new_surface_rect.width or self.get_height() != new_surface_rect.height):
                alpha = background.get_alpha()
                background = pygame_transform.scale(
                    background, self.get_size())
                background.set_alpha(alpha)
            self._surface = background

    def set_alpha(self, value: int) -> None:
        self._surface.set_alpha(value)

    def get_alpha(self) -> Union[int, None]:
        return self._surface.get_alpha()

    def set_visible(self, value: bool) -> None:
        self._visible = value

    def get_visible(self) -> bool:
        return self._visible

    def set_auto_scale(self, value: bool) -> None:
        self._auto_scale = value

    def get_auto_scale(self) -> bool:
        return self._auto_scale

    def add_mouse_handler(self, handler: MouseEventHandler) -> None:
        self._mouse_handlers.append(handler)

    def remove_mouse_handler(self, handler: MouseEventHandler) -> None:
        if handler in self._mouse_handlers:
            self._mouse_handlers.remove(handler)

    def is_collide(self, x_y: Tuple[int, int]) -> bool:
        return (self._collision_rect.collidepoint(x_y)) and (self._surface.get_at((x_y[0] - self.get_x(), x_y[1] - self.get_y())).a != 0)

    def handle_input(self, event: Event) -> None:
        mouse_pos = pygame_mouse.get_pos()
        for handler in self._mouse_handlers:
            handler.handle_event(
                event, self.is_collide(mouse_pos))

    def fill(self, color: Color) -> None:
        self._surface.fill(color)

    def paint(self, root_surface: Surface, parent_pos: Tuple[int, int]) -> None:
        surface_rect = self._surface.get_rect()
        if self._auto_scale and (self.get_width() != surface_rect.width or self.get_height() != surface_rect.height):
            alpha = self._surface.get_alpha()
            self._surface = pygame_transform.scale(
                self._surface, self.get_size())
            self._surface.set_alpha(alpha)
        if self._visible:
            root_surface.blit(
                self._surface, (parent_pos[0] + self.get_x(), parent_pos[1] + self.get_y()))
