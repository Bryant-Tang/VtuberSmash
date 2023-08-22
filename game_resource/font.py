import os
from pygame.font import Font

from .constants import File as FileName


DEFAULT: str = FileName.FONT_DEFAULT

_loaded_fonts = {}


def get_font(font_name: str, size: int) -> Font:
    global _loaded_fonts
    if (font_name, size) not in _loaded_fonts:
        path = os.path.join(FileName.FOLDER_ASSET,
                            FileName.FOLDER_FONT, font_name)
        _loaded_fonts[(font_name, size)] = Font(path, size)
    return _loaded_fonts[(font_name, size)]
