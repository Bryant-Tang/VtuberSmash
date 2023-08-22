from typing import List, Tuple, Union

from .component import Component, Surface, Rect, Event


class Box(Component):
    _children: List[Component]

    def __init__(self, background: Surface, rect: Rect = None) -> None:
        super().__init__(background, rect)
        self._children = []

    def add_component(self, comp: Component, index: int = -1) -> None:
        if index < 0:
            self._children.append(comp)
        else:
            self._children.insert(index, comp)

    def get_component_index(self, comp: Component) -> Union[int, None]:
        if comp in self._children:
            return self._children.index(comp)
        else:
            return None

    def is_component_in(self, comp: Component) -> bool:
        return (comp in self._children)

    def get_components(self) -> List[Component]:
        return self._children

    def pop_component(self) -> Union[Component, None]:
        if len(self._children) > 0:
            return self._children.pop()
        else:
            return None

    def remove_component(self, comp: Component) -> None:
        if comp in self._children:
            self._children.remove(comp)

    def clear_component(self) -> None:
        self._children.clear()

    def handle_input(self, event: Event) -> None:
        super().handle_input(event)
        for comp in self._children:
            comp.handle_input(event)

    def paint(self, root_surface: Surface, parent_pos: Tuple[int, int]) -> None:
        super().paint(root_surface, parent_pos)
        for comp in self._children:
            comp.paint(
                root_surface, (parent_pos[0] + self.get_x(), parent_pos[1] + self.get_y()))
