from typing import Callable, Dict, List
import source

from .player import Player
from .player_attribute import Attribute
from .card import Card
from . import card_factory
from .player_effect import VomitSugar, FullSugar

effect_dict: Dict[int, Callable[[bool], None]] = {}

_get_player_card_list: Callable[[], List[Card]]
_get_player_remain_card_list: Callable[[], List[Card]]
_get_enemy_card_list: Callable[[], List[Card]]
_get_enemy_remain_card_list: Callable[[], List[Card]]
_get_player: Callable[[], Player]
_get_enemy: Callable[[], Player]
_get_current_round: Callable[[], int]


def is_contain_card(card_list: List[Card], id: int) -> bool:
    for card in card_list:
        if card.get_id() == id:
            return True
    return False


def find_extra_card(card_list: List[Card], remain_card_list: List[Card]):
    if is_contain_card(card_list, 5) and is_contain_card(card_list, 6) and is_contain_card(card_list, 7):
        remain_card_list.append(card_factory.get_card(999))
    if is_contain_card(card_list, 8) and is_contain_card(card_list, 9):
        remain_card_list.append(card_factory.get_card(997))
    if is_contain_card(card_list, 10) and is_contain_card(card_list, 11):
        remain_card_list.append(card_factory.get_card(998))


def do_effect(id: int, is_from_player: bool) -> None:
    effect_dict[id](is_from_player)


def init(get_player_card_list: Callable[[], List[Card]], get_player_remain_card_list: Callable[[], List[Card]],
         get_enemy_card_list: Callable[[], List[Card]], get_enemy_remain_card_list: Callable[[], List[Card]],
         get_player: Callable[[], Player], get_enemy: Callable[[], Player], get_current_round: Callable[[], int]):
    global _get_player_card_list
    global _get_player_remain_card_list
    global _get_enemy_card_list
    global _get_enemy_remain_card_list
    global _get_player
    global _get_enemy
    global _get_current_round
    _get_player_card_list = get_player_card_list
    _get_player_remain_card_list = get_player_remain_card_list
    _get_enemy_card_list = get_enemy_card_list
    _get_enemy_remain_card_list = get_enemy_remain_card_list
    _get_player = get_player
    _get_enemy = get_enemy
    _get_current_round = get_current_round
    effect_dict[0] = effect_000
    effect_dict[1] = effect_001
    effect_dict[2] = effect_002
    effect_dict[3] = effect_003
    effect_dict[4] = effect_004
    effect_dict[5] = effect_005
    effect_dict[6] = effect_006
    effect_dict[7] = effect_007
    effect_dict[8] = effect_008
    effect_dict[9] = effect_009
    effect_dict[10] = effect_010
    effect_dict[11] = effect_011
    effect_dict[600] = effect_600
    effect_dict[601] = effect_601
    effect_dict[602] = effect_602
    effect_dict[603] = effect_603
    effect_dict[604] = effect_604
    effect_dict[997] = effect_997
    effect_dict[998] = effect_998
    effect_dict[999] = effect_999


def get_parm(is_from_player: bool):
    if is_from_player:
        player_card_list = _get_player_card_list()
        player_remain_card_list = _get_player_remain_card_list()
        enemy_card_list = _get_enemy_card_list()
        enemy_remain_card_list = _get_enemy_remain_card_list()
        player = _get_player()
        enemy = _get_enemy()
        current_round = _get_current_round()
    else:
        player_card_list = _get_enemy_card_list()
        player_remain_card_list = _get_enemy_remain_card_list()
        enemy_card_list = _get_player_card_list()
        enemy_remain_card_list = _get_player_remain_card_list()
        player = _get_enemy()
        enemy = _get_player()
        current_round = _get_current_round()
    return player_card_list, player_remain_card_list, enemy_card_list, enemy_remain_card_list, player, enemy, current_round


def effect_000(is_from_player: bool):
    _, _, _, _, _, enemy, _ = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_OUMUA_ANGRY).play()
    enemy.modify_attributes(Attribute.SHIELD, -8)


def effect_001(is_from_player: bool):
    _, _, _, _, _, enemy, _ = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_CYGNUS_WTF).play()
    enemy.modify_attributes(Attribute.HP, -4)


def effect_002(is_from_player: bool):
    _, _, _, _, player, _, _ = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_D2_LOVEU).play()
    player.modify_attributes(Attribute.HP, 4)


def effect_003(is_from_player: bool):
    _, _, _, _, player, _, _ = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_NEMO_CHARM).play()
    player.modify_attributes(Attribute.SHIELD, 8)


def effect_004(is_from_player: bool):
    _, _, _, _, player, enemy, _ = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_SPRINGFISH_DEADGE).play()
    enemy.modify_attributes(Attribute.HP, -3)
    enemy.modify_attributes(Attribute.SHIELD, -6)
    player.modify_attributes(Attribute.HP, -2)


def effect_005(is_from_player: bool):
    _, player_remain_card_list, _, _, _, enemy, _ = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_15_SHOOT).play()
    enemy.modify_attributes(Attribute.SHIELD, -6)
    player_remain_card_list.append(card_factory.get_card(5))


def effect_006(is_from_player: bool):
    _, player_remain_card_list, _, _, _, enemy, _ = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_LUTRA_ANGRY).play()
    enemy.modify_attributes(Attribute.HP, -3)
    player_remain_card_list.append(card_factory.get_card(6))

def effect_007(is_from_player: bool):
    _, player_remain_card_list, _, _, player, _, _ = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_OBEAR_SHUTUP).play()
    player.modify_attributes(Attribute.HP, 3)
    player_remain_card_list.append(card_factory.get_card(7))

def effect_008(is_from_player: bool):
    player_card_list, _, _, _, _, _, _ = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_SEKI_5MA).play()
    for _ in range(5):
        player_card_list.append(card_factory.get_card(600))


def effect_009(is_from_player: bool):
    _, _, _, _, player, enemy, _ = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_KSP_7414).play()
    enemy.modify_attributes(Attribute.SHIELD, -7)
    enemy.modify_attributes(Attribute.HP, -4)
    player.modify_attributes(Attribute.SHIELD, 1)
    player.modify_attributes(Attribute.HP, -4)


def effect_010(is_from_player: bool):
    _, _, _, _, player, enemy, _ = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_YANHUA_BABY).play()
    enemy.modify_attributes(Attribute.HP, -2)
    player.modify_attributes(Attribute.HP, 2)


def effect_011(is_from_player: bool):
    _, _, _, _, player, enemy, _ = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_QTTSIX_LOVEYANHUA).play()
    enemy.modify_attributes(Attribute.SHIELD, -4)
    player.modify_attributes(Attribute.SHIELD, 4)


def effect_600(is_from_player: bool):
    _, _, _, _, player, _, _ = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_APEX_POPHEALTH).play()
    player.modify_attributes(Attribute.HP, 1)


def effect_601(is_from_player: bool):
    _, _, _, _, player, _, _ = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_APEX_POPHEALTH).play()
    player.modify_attributes(Attribute.HP, 3)


def effect_602(is_from_player: bool):
    _, _, _, _, player, _, _ = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_APEX_POPBAT).play()
    player.modify_attributes(Attribute.SHIELD, 2)


def effect_603(is_from_player: bool):
    _, _, _, _, player, _, _ = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_APEX_POPBAT).play()
    player.modify_attributes(Attribute.SHIELD, 6)


def effect_604(is_from_player: bool):
    _, _, _, _, player, _, _ = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_APEX_POPPHINIX).play()
    player.modify_attributes(Attribute.HP, 2)
    player.modify_attributes(Attribute.SHIELD, 3)


def effect_997(is_from_player: bool):
    _, _, _, _, player, enemy, current_round = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_KSEKI_LOVEEACHOTHER).play()
    player.modify_attributes(Attribute.HP, 5)
    player.modify_attributes(Attribute.SHIELD, 2)
    enemy.modify_attributes(Attribute.HP, 0)
    enemy.add_effect(VomitSugar(current_round, 999))


def effect_998(is_from_player: bool):
    _, _, _, _, player, enemy, current_round = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_QTTSIXYANHUA_LOVERS).play()
    enemy.modify_attributes(Attribute.HP, -1)
    enemy.modify_attributes(Attribute.SHIELD, -3)
    player.modify_attributes(Attribute.HP, 1)
    player.modify_attributes(Attribute.SHIELD, 4)
    player.add_effect(FullSugar(current_round, 999))


def effect_999(is_from_player: bool):
    _, _, _, _, player, enemy, _ = get_parm(is_from_player)
    source.audio.get_sound(source.audio.EFFECT_RESCUTE_NONEEDPOOP).play()
    enemy.modify_attributes(Attribute.HP, -2)
    enemy.modify_attributes(Attribute.SHIELD, -3)
    player.modify_attributes(Attribute.HP, 2)
    player.modify_attributes(Attribute.SHIELD, 3)

# def effect_000(is_from_player: bool):
#     player_card_list, player_remain_card_list, enemy_card_list, enemy_remain_card_list, player, enemy, current_round = get_parm(is_from_player)
#     source.audio.get_sound(source.audio.EFFECT_RESCUTE_NONEEDPOOP).play()
