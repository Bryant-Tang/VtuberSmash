from gui_components import Component
import source

from .card import Card


def get_card(id: int):
    card = Card(source.image.card(id), id, id)
    card.set_size((source.constants.CARD_WIDTH, source.constants.CARD_HEIGHT))
    return card


def get_detail(id: int):
    return Component(source.image.card_detail(id))
