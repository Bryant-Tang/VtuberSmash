from .component import Component
from .box import Box, Surface
from .label import Label
from game_resource import constants, image


class Card(Box):
    _mask: Box
    _mask_label: Label
    _lock_sign: Component

    def __init__(self, background: Surface) -> None:
        super().__init__(background)
        self._mask = Box(Surface(self.get_size()))
        self._mask.set_alpha(constants.CARD_MASK_ALPHA)
        self._mask.fill(constants.COLOR_GRAY)
        self._mask_label = Label("", constants.COLOR_WHITE)
        self._mask.add_component(self._mask_label)
        self._lock_sign = Component(image.get_image(image.CARD_LOCK))
        self._lock_sign.set_center((self.get_width()//2,
                                    self.get_height()//2))

    def set_mask(self, text: str):
        self._mask_label.set_text(text)
        self._mask_label.set_center(
            (self._mask.get_width()//2, self._mask.get_height()//2))
        if self._mask not in self.get_components():
            self.add_component(self._mask)

    def remove_mask(self):
        self.remove_component(self._mask)

    def set_lock_sign(self):
        self.add_component(self._lock_sign)

    def remove_lock_sign(self):
        self.remove_component(self._lock_sign)
