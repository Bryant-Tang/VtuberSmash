from typing import List

from .box import Box, Surface, Component


class ValueBar(Box):
    _content_per_value: Surface
    _spacing: int
    _block_list: List[Component]

    def __init__(self, content_per_value: Surface, initial_value: int = 10, spacing: int = 0) -> None:
        super().__init__(Surface((0, 0)))
        self._spacing = spacing
        self._content_per_value = content_per_value
        self._block_list = []
        self.set_visible(False)
        self.set_width(0)
        self.set_height(content_per_value.get_rect().height)
        self.set_value(initial_value)

    def _add_block(self) -> None:
        block = Component(self._content_per_value)
        if len(self._block_list) == 0:
            block.set_x(0)
            self.set_width(block.get_width())
        else:
            block.set_x(self._block_list[-1].get_right() + self._spacing)
            self.set_width(self.get_width() +
                           self._spacing + block.get_width())
        self.add_component(block)
        self._block_list.append(block)

    def _remove_block(self) -> None:
        pop_block = self.pop_component()
        if pop_block in self._block_list:
            self._block_list.remove(pop_block)
            self.set_width(max(0, self.get_width() -
                           self._spacing - pop_block.get_width()))

    def set_value(self, value: int) -> None:
        if value > len(self._block_list):
            for _ in range(value - len(self._block_list)):
                self._add_block()
        elif value < len(self._block_list):
            for _ in range(len(self._block_list) - value):
                self._remove_block()

    def get_value(self) -> int:
        return len(self._block_list)
