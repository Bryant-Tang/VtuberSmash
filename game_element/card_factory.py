from typing import Dict, List, Union
from .card import Card
from game_resource import image, audio
from gui_components import Component
from pygame.mixer import Sound

from .effect_factory import CardEffectCreatingInformation, PlayerEffectCreatingInformation, get_card_effect

_card_initial_attribute: Dict[int, Dict[str,
                                        Union[List[CardEffectCreatingInformation], Sound]]]
_extra_card_id_dict: Dict[int, List[int]]


def init():
    global _card_initial_attribute
    global _extra_card_id_dict
    _card_initial_attribute = {
        0: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_SHIELD,
                    -8,
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_OUMUA_ANGRY),
        },
        1: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_HP,
                    -4,
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_CYGNUS_WTF),
        },
        2: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_HP,
                    4,
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_D2_LOVEU),
        },
        3: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_SHIELD,
                    8,
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_NEMO_CHARM),
        },
        4: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_HP,
                    -3,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_SHIELD,
                    -6,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_PLAYER_HP,
                    -2,
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_SPRINGFISH_DEADGE),
        },
        5: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_SHIELD,
                    -6,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_REMAIN_CARD,
                    (
                        [5],
                        -1,
                    ),
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_15_SHOOT),
        },
        6: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_HP,
                    -3,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_REMAIN_CARD,
                    ([6], -1),
                    1.0,
                ),
            ],
            "attack_sound":    audio.get_sound(audio.EFFECT_LUTRA_ANGRY),
        },
        7: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_HP,
                    3,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_REMAIN_CARD,
                    (
                        [7],
                        -1,
                    ),
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_OBEAR_SHUTUP),
        },
        8: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_ATTACK_CARD,
                    (
                        [600, 600, 600, 600, 600],
                        -1,
                    ),
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_SEKI_5MA),
        },
        9: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_SHIELD,
                    -7,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_HP,
                    -4,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_SHIELD,
                    1,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_PLAYER_HP,
                    -4,
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_KSP_7414),
        },
        10: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_HP,
                    -2,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_HP,
                    2,
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_YANHUA_BABY),
        },
        11: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_SHIELD,
                    -4,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_SHIELD,
                    4,
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_QTTSIX_LOVEYANHUA),
        },
        12: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_SHIELD,
                    0,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_HP,
                    -8,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_SHIELD,
                    0,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_PLAYER_HP,
                    -9,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_ATTACK_CARD,
                    (
                        [603, 603],
                        -1,
                    ),
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_REN_BEIDOL),
        },
        13: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_EFFECT_TO_PLAYER,
                    PlayerEffectCreatingInformation(
                        PlayerEffectCreatingInformation.APEX_PREDATOR,
                        3,
                        PlayerEffectCreatingInformation.CURRENT_ROUND,
                    ),
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_RESTIA_PAYTHEPRICE),
        },
        14: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_HP,
                    -2,
                    0.8,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_HP,
                    -2,
                    0.8,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_HP,
                    -2,
                    0.4,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_JONGIE_BOMBOMBITCH),
        },
        15: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_EFFECT_TO_PLAYER,
                    PlayerEffectCreatingInformation(
                        PlayerEffectCreatingInformation.GOOD_AT_TAKE_OFF_SHIRT,
                        1,
                        PlayerEffectCreatingInformation.CURRENT_ROUND,
                    ),
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_MARGARET_UNBUTTON),
        },
        16: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_ENEMY_ATTACK_CARD,
                    (
                        [605, 605, 605],
                        -1,
                    ),
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_LINGLAN_WOOFWOOF),
        },
        600: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_HP,
                    1,
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_APEX_POPHEALTH),
        },
        601: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_HP,
                    3,
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_APEX_POPHEALTH),
        },
        602: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_SHIELD,
                    2,
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_APEX_POPBAT),
        },
        603: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_SHIELD,
                    6,
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_APEX_POPBAT),
        },
        604: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_HP,
                    2,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_SHIELD,
                    3,
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_APEX_POPPHINIX),
        },
        605: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_PLAYER_HP,
                    -1,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_PLAYER_SHIELD,
                    -1,
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_LINGLAN_DARKCUISINE),
        },
        606: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_HP,
                    1,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_SHIELD,
                    1,
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_RC_WATERMELONMILK),
        },
        994: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_EFFECT_TO_ENEMY,
                    PlayerEffectCreatingInformation(
                        PlayerEffectCreatingInformation.VOMIT_SUGAR,
                        999,
                        f"{PlayerEffectCreatingInformation.CURRENT_ROUND} + 5",
                    ),
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_EFFECT_TO_PLAYER,
                    PlayerEffectCreatingInformation(
                        PlayerEffectCreatingInformation.FULL_SUGAR,
                        999,
                        f"{PlayerEffectCreatingInformation.CURRENT_ROUND} + 5",
                    ),
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_MARGARET_AHHHHH),
        },
        995: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_ATTACK_CARD,
                    (
                        [606],
                        0,
                    ),
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_ATTACK_CARD,
                    (
                        [995],
                        0,
                    ),
                    0.786,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_RC_YOUAREGOOD),
        },
        996: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_HP,
                    3,
                    0.583,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_SHIELD,
                    6,
                    0.583,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_SHIELD,
                    -6,
                    0.583,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_HP,
                    -3,
                    0.583,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_RSD2_RE45YEAH),
        },
        997: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_HP,
                    5,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_SHIELD,
                    2,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_HP,
                    0,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_EFFECT_TO_ENEMY,
                    PlayerEffectCreatingInformation(
                        PlayerEffectCreatingInformation.VOMIT_SUGAR,
                        999,
                        PlayerEffectCreatingInformation.CURRENT_ROUND,
                    ),
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_KSEKI_LOVEEACHOTHER),
        },
        998: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_HP,
                    -1,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_SHIELD,
                    -3,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_HP,
                    1,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_SHIELD,
                    4,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_EFFECT_TO_PLAYER,
                    PlayerEffectCreatingInformation(
                        PlayerEffectCreatingInformation.FULL_SUGAR,
                        999,
                        PlayerEffectCreatingInformation.CURRENT_ROUND,
                    ),
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_QTTSIXYANHUA_LOVERS),
        },
        999: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_HP,
                    -3,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_SHIELD,
                    -4,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_HP,
                    3,
                    1.0,
                ),
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.ADD_PLAYER_SHIELD,
                    4,
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_RESCUTE_NONEEDPOOP),
        },
        1000: {
            "effect_creating_information_list": [
                CardEffectCreatingInformation(
                    CardEffectCreatingInformation.REDUCE_ENEMY_HP,
                    -999,
                    1.0,
                ),
            ],
            "attack_sound": audio.get_sound(audio.EFFECT_EMOTIONAL_DAMAGE),
        },
    }
    _extra_card_id_dict = {
        999: [5, 6, 7],
        998: [10, 11],
        997: [8, 9],
        996: [2, 13],
        995: [1, 12],
        994: [15, 16],
    }


def find_extra_card(card_list: List[Card]):
    matching_extra_card_list: List[Card] = []
    card_id_list = [card.get_card_id() for card in card_list]
    for extra_card_id, extra_card_group_card_id_list in _extra_card_id_dict.items():
        if all(card_id in card_id_list for card_id in extra_card_group_card_id_list):
            matching_extra_card_list.append(get_card(extra_card_id))
    return matching_extra_card_list


def get_card(card_id: int):
    if card_id not in _card_initial_attribute.keys():
        raise ValueError(f"{card_id} is an invalid card id")
    effect_creating_information_list = _card_initial_attribute[
        card_id]["effect_creating_information_list"]
    attack_sound = _card_initial_attribute[card_id]["attack_sound"]
    if not (isinstance(effect_creating_information_list, list) and all(isinstance(item, CardEffectCreatingInformation) for item in effect_creating_information_list)):
        raise TypeError(
            f"Initialize error, Expected an List[PlayerEffectCreatingInformation] for effect_creating_information_list, got {type(effect_creating_information_list).__name__}")
    if not isinstance(attack_sound, Sound):
        raise TypeError(
            f"Initialize error, Expected an Sound for attack_sound, got {type(attack_sound).__name__}")
    return Card(card_id, image.card(card_id), [get_card_effect(creating_information) for creating_information in effect_creating_information_list], attack_sound)


def get_card_detail(card_id: int):
    return Component(image.card_detail(card_id))


def get_all_card_id():
    return [card_id for card_id in _card_initial_attribute.keys() if card_id < 1000]


def get_all_extra_card_id():
    return [card_id for card_id in _extra_card_id_dict.keys()]
