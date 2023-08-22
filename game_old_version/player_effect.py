from typing import Callable, Dict, List
from gui_components import Component

from .player import Player
from .card import Card


# class EffectTarget:
#     def add_hp(self, value: int):
#         pass

#     def add_shield(self, value: int):
#         pass

effect_dict: Dict[int, Callable[[bool], None]] = {}

_add_effect_icon: Callable[[Component,], None]
_get_player_card_list: Callable[[Player], List[Card]]
_get_player_remain_card_list: Callable[[Player], List[Card]]
_get_enemy_card_list: Callable[[Player], List[Card]]
_get_enemy_remain_card_list: Callable[[Player], List[Card]]
_get_enemy: Callable[[Player], Player]
_get_current_round: Callable[[], int]


def init(add_effect_icon: Callable[[Component], None],
         get_player_card_list: Callable[[Player], List[Card]], get_player_remain_card_list: Callable[[Player], List[Card]],
         get_enemy_card_list: Callable[[Player], List[Card]], get_enemy_remain_card_list: Callable[[Player], List[Card]],
         get_player: Callable[[Player], Player], get_enemy: Callable[[Player], Player], get_current_round: Callable[[], int]):
    global _add_effect_icon
    global _get_player_card_list
    global _get_player_remain_card_list
    global _get_enemy_card_list
    global _get_enemy_remain_card_list
    global _get_player
    global _get_enemy
    global _get_current_round
    _add_effect_icon = add_effect_icon
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


def do_effect(id: int, is_from_player: bool):
    effect_dict[id](is_from_player)

# def _simple_add_effect_icon(icon: Component):
#     threading.Thread(target=_add_effect_icon, args=(icon,)).start()


# class PlayerEffect:
#     BEFORE_MODIFY_VALUE: str = "before_modify_value"
#     AFTER_MODIFY_VALUE: str = "after_modify_value"
#     BEFORE_ROUND: str = "before_round"
#     AFTER_ROUND: str = "after_round"
#     BEFORE_CARD: str = "before_card"
#     AFTER_CARD: str = "after_card"
#     _max_round: int
#     _max_times: int
#     _icon: Component
#     _is_fail: bool
#     _timing_list: List[str]

#     def __init__(self, max_round: int,  max_times: int, icon: Component) -> None:
#         self._max_round = max_round
#         self._max_times = max_times
#         self._icon = icon
#         self._is_fail = False
#         self._timing_list = []

#     def is_contain_timing(self, timing: str):
#         return timing in self._timing_list

#     def is_fail(self):
#         return self._is_fail

#     def do_effect(self, player: EffectTarget, modifing_attribute: str, modifing_value: int, timing: str):
#         if (_get_current_round() > self._max_round):
#             self._is_fail = True
#             return modifing_attribute, modifing_value
#         if (not self._is_fail) and self._check_condition(player, modifing_attribute, modifing_value, timing):
#             modifing_attribute, modifing_value = self._do_effect(
#                 player, modifing_attribute, modifing_value)
#         if timing == PlayerEffect.AFTER_ROUND and (_get_current_round() >= self._max_round):
#             self._is_fail = True
#         return modifing_attribute, modifing_value

#     def _check_condition(self, player: EffectTarget, modifing_attribute: str, modifing_value: int, timing: str) -> bool:
#         return False

#     def _do_effect(self, player: EffectTarget, modifing_attribute: str, modifing_value: int):
#         _simple_add_effect_icon(self._icon)
#         self._max_times -= 1
#         if self._max_times <= 0:
#             self._is_fail = True
#         return modifing_attribute, modifing_value

#     def get_max_round(self) -> int:
#         return self._max_round

#     def get_max_times(self) -> int:
#         return self._max_times


# class VomitSugar(PlayerEffect):
#     def __init__(self, max_round: int,  max_times: int) -> None:
#         super().__init__(max_round, max_times,
#                          Component(source.image.get_image(source.image.EFFECT_VOMIT_SUGAR)))
#         self._timing_list.extend([PlayerEffect.AFTER_MODIFY_VALUE])

#     def _check_condition(self, player: EffectTarget, modifing_attribute: str, modifing_value: int, timing: str) -> bool:
#         return (timing == PlayerEffect.AFTER_MODIFY_VALUE) and (modifing_attribute == Attribute.HP)

#     def _do_effect(self, player: EffectTarget, modifing_attribute: str, modifing_value: int):
#         player.add_hp(-1)
#         return super()._do_effect(player, modifing_attribute, modifing_value)


# class FullSugar(PlayerEffect):
#     def __init__(self, max_round: int,  max_times: int) -> None:
#         super().__init__(max_round,  max_times,
#                          Component(source.image.get_image(source.image.EFFECT_FULL_SUGAR)))
#         self._timing_list.extend([PlayerEffect.AFTER_MODIFY_VALUE])

#     def _check_condition(self, player: EffectTarget, modifing_attribute: str, modifing_value: int, timing: str) -> bool:
#         return (timing == PlayerEffect.AFTER_MODIFY_VALUE) and (modifing_attribute == Attribute.HP)

#     def _do_effect(self, player: EffectTarget, modifing_attribute: str, modifing_value: int):
#         player.add_hp(1)
#         return super()._do_effect(player, modifing_attribute, modifing_value)


# class ApexPredator(PlayerEffect):
#     def __init__(self, max_round: int,  max_times: int) -> None:
#         super().__init__(max_round,  max_times,
#                          Component(source.image.get_image(source.image.EFFECT_FULL_SUGAR)))
#         self._timing_list.extend([PlayerEffect.BEFORE_CARD])

#     def _check_condition(self, player: EffectTarget, modifing_attribute: str, modifing_value: int, timing: str) -> bool:
#         return (timing == PlayerEffect.BEFORE_CARD)

#     def _do_effect(self, player: EffectTarget, modifing_attribute: str, modifing_value: int):
#         enemy = _get_enemy(player)
#         enemy.add_hp(-2)
#         return super()._do_effect(player, modifing_attribute, modifing_value)


# class GreatAtTakeOffCloth(PlayerEffect):
#     def __init__(self, max_round: int,  max_times: int) -> None:
#         super().__init__(max_round,  max_times,
#                          Component(source.image.get_image(source.image.EFFECT_FULL_SUGAR)))
#         self._timing_list.extend([PlayerEffect.BEFORE_MODIFY_VALUE])

#     def _check_condition(self, player: EffectTarget, modifing_attribute: str, modifing_value: int, timing: str) -> bool:
#         return (timing == PlayerEffect.BEFORE_MODIFY_VALUE) and (modifing_attribute == Attribute.SHIELD) and (modifing_value < 0)

#     def _do_effect(self, player: EffectTarget, modifing_attribute: str, modifing_value: int):
#         enemy = _get_enemy(player)
#         enemy.add_hp(-2)
#         return super()._do_effect(player, modifing_attribute, modifing_value)
