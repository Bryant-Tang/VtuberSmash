from typing import Tuple

from .box import Box, Surface


class Scene(Box):
    def __init__(self, background: Surface = None, size: Tuple[int, int] = (0, 0)) -> None:
        if background:
            super().__init__(background)
        else:
            super().__init__(Surface((0, 0)))
        if size[0] != 0 or size[1] != 0:
            self.set_size(size)

    def set_pos(self, x_y: Tuple[int, int]) -> None:
        return super().set_pos((0, 0))

    def set_center(self, x_y: Tuple[int, int]) -> None:
        return super().set_center(self.get_center())

    def start_showing(self):
        ''''''
        pass
