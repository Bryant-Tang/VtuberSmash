from .effect_factory import init as effect_factory_init
from .card_factory import init as card_factory_init, get_card
from .player_factory import init as player_factory_init


def init():
    card_factory_init()
    player_factory_init()
    effect_factory_init(get_card)
