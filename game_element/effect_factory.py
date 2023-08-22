from typing import Any, Callable, List, Tuple, Union
from game_logic import AffectableAttribute, AffectableOperation, AffectableTarget, AffectableTiming
from gui_components import Surface
from game_resource import image

from .card import Card
from .player import Player
from .card_effect import CardEffect
from .palyer_effect import PlayerEffect
from .creating_information import CardEffectCreatingInformation, PlayerEffectCreatingInformation

_get_card: Callable[[int], Card]


def init(get_card: Callable[[int], Card]):
    global _get_card
    _get_card = get_card


class AddPlayerHpCardEffect(CardEffect):
    def __init__(self, affect_value: int,  affect_probability: float) -> None:
        super().__init__(AffectableTarget.OUR_SIDE_PLAYER, AffectableAttribute.HP, AffectableOperation.ADD_INT, AffectableTiming.PERFORM_CARD_ATTACK,
                         affect_value, affect_probability, Surface((0, 0)), CardEffectCreatingInformation.ADD_PLAYER_HP)

    def check_conditon(self, timing: str, current_round: int) -> bool:
        super_result = super().check_conditon()
        return super_result and timing == self.affect_timing

    def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int):
        our_side_player.add_hp(self.affect_value)
        return super().do_effect(our_side_player, enemy_side_player, current_round)

    def get_creating_information(self):
        return CardEffectCreatingInformation(CardEffectCreatingInformation.ADD_PLAYER_HP, self.affect_value, self.affect_probability)

    def __reduce__(self):
        return (get_card_effect, (self.get_creating_information(),))


class AddPlayerShieldCardEffect(CardEffect):
    def __init__(self, affect_value: int,  affect_probability: float) -> None:
        super().__init__(AffectableTarget.OUR_SIDE_PLAYER, AffectableAttribute.SHIELD, AffectableOperation.ADD_INT, AffectableTiming.PERFORM_CARD_ATTACK,
                         affect_value, affect_probability, Surface((0, 0)), CardEffectCreatingInformation.ADD_PLAYER_SHIELD)

    def check_conditon(self, timing: str, current_round: int) -> bool:
        super_result = super().check_conditon()
        return super_result and timing == self.affect_timing

    def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int):
        our_side_player.add_shield(self.affect_value)
        return super().do_effect(our_side_player, enemy_side_player, current_round)

    def __reduce__(self):
        return (get_card_effect, (self.get_creating_information(),))


class AddEnemyHpCardEffect(CardEffect):
    def __init__(self, affect_value: int,  affect_probability: float) -> None:
        super().__init__(AffectableTarget.ENEMY_SIDE_PLAYER, AffectableAttribute.HP, AffectableOperation.ADD_INT, AffectableTiming.PERFORM_CARD_ATTACK,
                         affect_value, affect_probability, Surface((0, 0)), CardEffectCreatingInformation.ADD_ENEMY_HP)

    def check_conditon(self, timing: str, current_round: int) -> bool:
        super_result = super().check_conditon()
        return super_result and timing == self.affect_timing

    def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int):
        enemy_side_player.add_hp(self.affect_value)
        return super().do_effect(our_side_player, enemy_side_player, current_round)

    def __reduce__(self):
        return (get_card_effect, (self.get_creating_information(),))


class AddEnemyShieldCardEffect(CardEffect):
    def __init__(self, affect_value: int,  affect_probability: float) -> None:
        super().__init__(AffectableTarget.ENEMY_SIDE_PLAYER, AffectableAttribute.SHIELD, AffectableOperation.ADD_INT, AffectableTiming.PERFORM_CARD_ATTACK,
                         affect_value, affect_probability, Surface((0, 0)), CardEffectCreatingInformation.ADD_ENEMY_SHIELD)

    def check_conditon(self, timing: str, current_round: int) -> bool:
        super_result = super().check_conditon()
        return super_result and timing == self.affect_timing

    def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int):
        enemy_side_player.add_shield(self.affect_value)
        return super().do_effect(our_side_player, enemy_side_player, current_round)

    def __reduce__(self):
        return (get_card_effect, (self.get_creating_information(),))


class ReducePlayerHpCardEffect(CardEffect):
    def __init__(self, affect_value: int,  affect_probability: float) -> None:
        super().__init__(AffectableTarget.OUR_SIDE_PLAYER, AffectableAttribute.HP, AffectableOperation.REDUCE_INT, AffectableTiming.PERFORM_CARD_ATTACK,
                         affect_value, affect_probability, Surface((0, 0)), CardEffectCreatingInformation.REDUCE_PLAYER_HP)

    def check_conditon(self, timing: str, current_round: int) -> bool:
        super_result = super().check_conditon()
        return super_result and timing == self.affect_timing

    def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int):
        our_side_player.add_hp(self.affect_value)
        return super().do_effect(our_side_player, enemy_side_player, current_round)

    def __reduce__(self):
        return (get_card_effect, (self.get_creating_information(),))


class ReducePlayerShieldCardEffect(CardEffect):
    def __init__(self, affect_value: int,  affect_probability: float) -> None:
        super().__init__(AffectableTarget.OUR_SIDE_PLAYER, AffectableAttribute.SHIELD, AffectableOperation.REDUCE_INT, AffectableTiming.PERFORM_CARD_ATTACK,
                         affect_value, affect_probability, Surface((0, 0)), CardEffectCreatingInformation.REDUCE_PLAYER_SHIELD)

    def check_conditon(self, timing: str, current_round: int) -> bool:
        super_result = super().check_conditon()
        return super_result and timing == self.affect_timing

    def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int):
        our_side_player.add_shield(self.affect_value)
        return super().do_effect(our_side_player, enemy_side_player, current_round)

    def __reduce__(self):
        return (get_card_effect, (self.get_creating_information(),))


class ReduceEnemyHpCardEffect(CardEffect):
    def __init__(self, affect_value: int,  affect_probability: float) -> None:
        super().__init__(AffectableTarget.ENEMY_SIDE_PLAYER, AffectableAttribute.HP, AffectableOperation.REDUCE_INT, AffectableTiming.PERFORM_CARD_ATTACK,
                         affect_value, affect_probability, Surface((0, 0)), CardEffectCreatingInformation.REDUCE_ENEMY_HP)

    def check_conditon(self, timing: str, current_round: int) -> bool:
        super_result = super().check_conditon()
        return super_result and timing == self.affect_timing

    def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int):
        enemy_side_player.add_hp(self.affect_value)
        return super().do_effect(our_side_player, enemy_side_player, current_round)

    def __reduce__(self):
        return (get_card_effect, (self.get_creating_information(),))


class ReduceEnemyShieldCardEffect(CardEffect):
    def __init__(self, affect_value: int,  affect_probability: float) -> None:
        super().__init__(AffectableTarget.ENEMY_SIDE_PLAYER, AffectableAttribute.SHIELD, AffectableOperation.REDUCE_INT, AffectableTiming.PERFORM_CARD_ATTACK,
                         affect_value, affect_probability, Surface((0, 0)), CardEffectCreatingInformation.REDUCE_ENEMY_SHIELD)

    def check_conditon(self, timing: str, current_round: int) -> bool:
        super_result = super().check_conditon()
        return super_result and timing == self.affect_timing

    def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int):
        enemy_side_player.add_shield(self.affect_value)
        return super().do_effect(our_side_player, enemy_side_player, current_round)

    def __reduce__(self):
        return (get_card_effect, (self.get_creating_information(),))


class AddPlayerAttackCardCardEffect(CardEffect):
    def __init__(self, affect_value: Tuple[List[int], int],  affect_probability: float) -> None:
        super().__init__(AffectableTarget.OUR_SIDE_PLAYER, AffectableAttribute.ATTACK_CARD_LIST, AffectableOperation.ADD_CARD, AffectableTiming.PERFORM_CARD_ATTACK,
                         affect_value, affect_probability, Surface((0, 0)), CardEffectCreatingInformation.ADD_PLAYER_ATTACK_CARD)

    def check_conditon(self, timing: str, current_round: int) -> bool:
        super_result = super().check_conditon()
        return super_result and timing == self.affect_timing

    def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int):
        card_id_list = self.affect_value[0]
        index = self.affect_value[1]
        if not (isinstance(card_id_list, list) and all(isinstance(item, int) for item in card_id_list)):
            raise TypeError(
                f"Expected an List[int] for self.affect_value[0], which is card_id_list, got {type(card_id_list).__name__}")
        if not isinstance(index, int):
            raise TypeError(
                f"Expected an int for self.affect_value[1], which is index, got {type(index).__name__}")
        if index == -1:
            for card_id in card_id_list:
                our_side_player.attack_card_list.append(_get_card(card_id))
        else:
            for card_id in card_id_list:
                our_side_player.attack_card_list.insert(
                    index, _get_card(card_id))
                index += 1
        return super().do_effect(our_side_player, enemy_side_player, current_round)

    def __reduce__(self):
        return (get_card_effect, (self.get_creating_information(),))


class AddPlayerRemainCardCardEffect(CardEffect):
    def __init__(self, affect_value: Tuple[List[int], int],  affect_probability: float) -> None:
        super().__init__(AffectableTarget.OUR_SIDE_PLAYER, AffectableAttribute.REMAIN_CARD_LIST, AffectableOperation.ADD_CARD, AffectableTiming.PERFORM_CARD_ATTACK,
                         affect_value, affect_probability, Surface((0, 0)), CardEffectCreatingInformation.ADD_PLAYER_REMAIN_CARD)

    def check_conditon(self, timing: str, current_round: int) -> bool:
        super_result = super().check_conditon()
        return super_result and timing == self.affect_timing

    def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int):
        card_id_list = self.affect_value[0]
        index = self.affect_value[1]
        if not (isinstance(card_id_list, list) and all(isinstance(item, int) for item in card_id_list)):
            raise TypeError(
                f"Expected an List[int] for self.affect_value[0], which is card_id_list, got {type(card_id_list).__name__}")
        if not isinstance(index, int):
            raise TypeError(
                f"Expected an int for self.affect_value[1], which is index, got {type(index).__name__}")
        if index == -1:
            for card_id in card_id_list:
                our_side_player.drawn_card_list.append(_get_card(card_id))
        else:
            for card_id in card_id_list:
                our_side_player.drawn_card_list.insert(
                    index, _get_card(card_id))
                index += 1
        return super().do_effect(our_side_player, enemy_side_player, current_round)

    def __reduce__(self):
        return (get_card_effect, (self.get_creating_information(),))


class AddEnemyAttackCardCardEffect(CardEffect):
    def __init__(self, affect_value: Tuple[List[int], int],  affect_probability: float) -> None:
        super().__init__(AffectableTarget.ENEMY_SIDE_PLAYER, AffectableAttribute.ATTACK_CARD_LIST, AffectableOperation.ADD_CARD, AffectableTiming.PERFORM_CARD_ATTACK,
                         affect_value, affect_probability, Surface((0, 0)), CardEffectCreatingInformation.ADD_ENEMY_ATTACK_CARD)

    def check_conditon(self, timing: str, current_round: int) -> bool:
        super_result = super().check_conditon()
        return super_result and timing == self.affect_timing

    def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int):
        card_id_list = self.affect_value[0]
        index = self.affect_value[1]
        if not (isinstance(card_id_list, list) and all(isinstance(item, int) for item in card_id_list)):
            raise TypeError(
                f"Expected an List[int] for self.affect_value[0], which is card_id_list, got {type(card_id_list).__name__}")
        if not isinstance(index, int):
            raise TypeError(
                f"Expected an int for self.affect_value[1], which is index, got {type(index).__name__}")
        if index == -1:
            for card_id in card_id_list:
                enemy_side_player.attack_card_list.append(_get_card(card_id))
        else:
            for card_id in card_id_list:
                enemy_side_player.attack_card_list.insert(
                    index, _get_card(card_id))
                index += 1
        return super().do_effect(our_side_player, enemy_side_player, current_round)

    def __reduce__(self):
        return (get_card_effect, (self.get_creating_information(),))


class AddEnemyRemainCardCardEffect(CardEffect):
    def __init__(self, affect_value: Tuple[List[int], int],  affect_probability: float) -> None:
        super().__init__(AffectableTarget.ENEMY_SIDE_PLAYER, AffectableAttribute.REMAIN_CARD_LIST, AffectableOperation.ADD_CARD, AffectableTiming.PERFORM_CARD_ATTACK,
                         affect_value, affect_probability, Surface((0, 0)), CardEffectCreatingInformation.ADD_ENEMY_REMAIN_CARD)

    def check_conditon(self, timing: str, current_round: int) -> bool:
        super_result = super().check_conditon()
        return super_result and timing == self.affect_timing

    def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int):
        card_id_list = self.affect_value[0]
        index = self.affect_value[1]
        if not (isinstance(card_id_list, list) and all(isinstance(item, int) for item in card_id_list)):
            raise TypeError(
                f"Expected an List[int] for self.affect_value[0], which is card_id_list, got {type(card_id_list).__name__}")
        if not isinstance(index, int):
            raise TypeError(
                f"Expected an int for self.affect_value[1], which is index, got {type(index).__name__}")
        if index == -1:
            for card_id in card_id_list:
                enemy_side_player.drawn_card_list.append(_get_card(card_id))
        else:
            for card_id in card_id_list:
                enemy_side_player.drawn_card_list.insert(
                    index, _get_card(card_id))
                index += 1
        return super().do_effect(our_side_player, enemy_side_player, current_round)

    def __reduce__(self):
        return (get_card_effect, (self.get_creating_information(),))


# class AddCardEffectToPlayerCardEffect(CardEffect):
#     def __init__(self, affect_value: CardEffectCreatingInformation, affect_probability: float) -> None:
#         super().__init__(AffectableTarget.OUR_SIDE_PLAYER, AffectableAttribute.EFFECT_LIST, AffectableOperation.ADD_EFFECT, AffectableTiming.PERFORM_CARD_ATTACK,
#                          affect_value,
#                          affect_probability, Surface((0, 0)), CardEffectCreatingInformation.)

#     def check_conditon(self, timing: str, current_round: int) -> bool:
#         super_result = super().check_conditon()
#         return super_result and timing == self.affect_timing

#     def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int):
#         if not isinstance(self.affect_value, PlayerEffectCreatingInformation):
#             raise TypeError(
#                 f"Expected an PlayerEffectCreatingInformation for self.affect_value, got {type(self.affect_value).__name__}")
#         creating_information = self.affect_value.copy()
#         if type(creating_information.max_round) is str:
#             creating_information.max_round = creating_information.max_round.replace(
#                 PlayerEffectCreatingInformation.CURRENT_ROUND, str(current_round))
#             caculate_result = eval(creating_information.max_round)

#             if not isinstance(caculate_result, int):
#                 raise TypeError(
#                     f"Expected an int for caculate_result, got {type(caculate_result).__name__}")
#             creating_information.max_round = caculate_result
#         our_side_player.player_effect_list.append(
#             get_player_effect(creating_information))
#         return super().do_effect(our_side_player, enemy_side_player, current_round)

class AddPlayerEffectToPlayerCardEffect(CardEffect):
    def __init__(self, affect_value: PlayerEffectCreatingInformation, affect_probability: float) -> None:
        super().__init__(AffectableTarget.OUR_SIDE_PLAYER, AffectableAttribute.EFFECT_LIST, AffectableOperation.ADD_EFFECT, AffectableTiming.PERFORM_CARD_ATTACK,
                         affect_value,
                         affect_probability, Surface((0, 0)), CardEffectCreatingInformation.ADD_PLAYER_EFFECT_TO_PLAYER)

    def check_conditon(self, timing: str, current_round: int) -> bool:
        super_result = super().check_conditon()
        return super_result and timing == self.affect_timing

    def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int):
        if not isinstance(self.affect_value, PlayerEffectCreatingInformation):
            raise TypeError(
                f"Expected an PlayerEffectCreatingInformation for self.affect_value, got {type(self.affect_value).__name__}")
        creating_information = self.affect_value.copy()
        if type(creating_information.max_round) is str:
            creating_information.max_round = creating_information.max_round.replace(
                PlayerEffectCreatingInformation.CURRENT_ROUND, str(current_round))
            caculate_result = eval(creating_information.max_round)

            if not isinstance(caculate_result, int):
                raise TypeError(
                    f"Expected an int for caculate_result, got {type(caculate_result).__name__}")
            creating_information.max_round = caculate_result
        our_side_player.player_effect_list.append(
            get_player_effect(creating_information))
        return super().do_effect(our_side_player, enemy_side_player, current_round)

    def __reduce__(self):
        return (get_card_effect, (self.get_creating_information(),))


class AddPlayerEffectToEnemyCardEffect(CardEffect):
    def __init__(self, affect_value: PlayerEffectCreatingInformation, affect_probability: float) -> None:
        super().__init__(AffectableTarget.ENEMY_SIDE_PLAYER, AffectableAttribute.EFFECT_LIST, AffectableOperation.ADD_EFFECT, AffectableTiming.PERFORM_CARD_ATTACK,
                         affect_value,
                         affect_probability, Surface((0, 0)), CardEffectCreatingInformation.ADD_PLAYER_EFFECT_TO_ENEMY)

    def check_conditon(self, timing: str, current_round: int) -> bool:
        super_result = super().check_conditon()
        return super_result and timing == self.affect_timing

    def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int):
        if not isinstance(self.affect_value, PlayerEffectCreatingInformation):
            raise TypeError(
                f"Expected an PlayerEffectCreatingInformation for self.affect_value, got {type(self.affect_value).__name__}")
        creating_information = self.affect_value.copy()
        if type(creating_information.max_round) is str:
            creating_information.max_round = creating_information.max_round.replace(
                PlayerEffectCreatingInformation.CURRENT_ROUND, str(current_round))
            caculate_result = eval(creating_information.max_round)

            if not isinstance(caculate_result, int):
                raise TypeError(
                    f"Expected an int for caculate_result, got {type(caculate_result).__name__}")
            creating_information.max_round = caculate_result
        enemy_side_player.player_effect_list.append(
            get_player_effect(creating_information))
        return super().do_effect(our_side_player, enemy_side_player, current_round)

    def __reduce__(self):
        return (get_card_effect, (self.get_creating_information(),))


class VomitSugarPlayerEffect(PlayerEffect):
    def __init__(self,  max_affect_times: int, max_affect_round: int) -> None:
        super().__init__(AffectableTiming.AFTER_CARD_EFFECT, max_affect_times, max_affect_round,
                         image.get_image(image.EFFECT_VOMIT_SUGAR), image.EFFECT_VOMIT_SUGAR, PlayerEffectCreatingInformation.VOMIT_SUGAR)

    def check_conditon(self, timing: str, current_round: int, our_side_card: Union[Card, None] = None, enemy_side_card: Union[Card, None] = None, our_side_card_effect: Union[CardEffect, None] = None, enemy_side_card_effect: Union[CardEffect, None] = None) -> bool:
        super_result = super().check_conditon(timing, current_round, our_side_card,
                                              enemy_side_card, our_side_card_effect, enemy_side_card_effect)
        return super_result and timing == self.affect_timing \
            and ((our_side_card_effect
                  and our_side_card_effect.affect_target == AffectableTarget.OUR_SIDE_PLAYER
                  and our_side_card_effect.affect_attribute == AffectableAttribute.HP
                  and (our_side_card_effect.affect_operation == AffectableOperation.REDUCE_INT
                       or our_side_card_effect.affect_operation == AffectableOperation.ADD_INT))
                 or (enemy_side_card_effect
                     and enemy_side_card_effect.affect_target == AffectableTarget.ENEMY_SIDE_PLAYER
                     and enemy_side_card_effect.affect_attribute == AffectableAttribute.HP
                     and (enemy_side_card_effect.affect_operation == AffectableOperation.REDUCE_INT
                          or enemy_side_card_effect.affect_operation == AffectableOperation.ADD_INT)))

    def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int, our_side_card: Union[Card, None] = None, enemy_side_card: Union[Card, None] = None, our_side_card_effect: Union[CardEffect, None] = None, enemy_side_card_effect: Union[CardEffect, None] = None) -> Union['Card', CardEffect, None]:
        super_result = super().do_effect(our_side_player, enemy_side_player, current_round,
                                         our_side_card, enemy_side_card, our_side_card_effect, enemy_side_card_effect)
        our_side_player.add_hp(-1)
        return super_result

    def __reduce__(self):
        return (get_player_effect, (self.get_creating_information(),))


class FullSugarPlayerEffect(PlayerEffect):
    def __init__(self,  max_affect_times: int, max_affect_round: int) -> None:
        super().__init__(AffectableTiming.AFTER_CARD_EFFECT, max_affect_times, max_affect_round,
                         image.get_image(image.EFFECT_FULL_SUGAR), image.EFFECT_FULL_SUGAR, PlayerEffectCreatingInformation.FULL_SUGAR)

    def check_conditon(self, timing: str, current_round: int, our_side_card: Union[Card, None] = None, enemy_side_card: Union[Card, None] = None, our_side_card_effect: Union[CardEffect, None] = None, enemy_side_card_effect: Union[CardEffect, None] = None) -> bool:
        super_result = super().check_conditon(timing, current_round, our_side_card,
                                              enemy_side_card, our_side_card_effect, enemy_side_card_effect)
        return super_result and timing == self.affect_timing \
            and ((our_side_card_effect
                  and our_side_card_effect.affect_target == AffectableTarget.OUR_SIDE_PLAYER
                  and our_side_card_effect.affect_attribute == AffectableAttribute.HP
                  and (our_side_card_effect.affect_operation == AffectableOperation.REDUCE_INT
                       or our_side_card_effect.affect_operation == AffectableOperation.ADD_INT))
                 or (enemy_side_card_effect
                     and enemy_side_card_effect.affect_target == AffectableTarget.ENEMY_SIDE_PLAYER
                     and enemy_side_card_effect.affect_attribute == AffectableAttribute.HP
                     and (enemy_side_card_effect.affect_operation == AffectableOperation.REDUCE_INT
                          or enemy_side_card_effect.affect_operation == AffectableOperation.ADD_INT)))

    def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int, our_side_card: Union[Card, None] = None, enemy_side_card: Union[Card, None] = None, our_side_card_effect: Union[CardEffect, None] = None, enemy_side_card_effect: Union[CardEffect, None] = None) -> Union['Card', CardEffect, None]:
        super_result = super().do_effect(our_side_player, enemy_side_player, current_round,
                                         our_side_card, enemy_side_card, our_side_card_effect, enemy_side_card_effect)
        our_side_player.add_hp(1)
        return super_result

    def __reduce__(self):
        return (get_player_effect, (self.get_creating_information(),))


class GoodAtTakeOffShirtPlayerEffect(PlayerEffect):
    def __init__(self,  max_affect_times: int, max_affect_round: int) -> None:
        super().__init__(AffectableTiming.BEFORE_CARD_EFFECT, max_affect_times, max_affect_round,
                         image.get_image(image.EFFECT_GOOD_AT_TAKE_OFF_SHIRT), image.EFFECT_GOOD_AT_TAKE_OFF_SHIRT, PlayerEffectCreatingInformation.GOOD_AT_TAKE_OFF_SHIRT)

    def check_conditon(self, timing: str, current_round: int, our_side_card: Union[Card, None] = None, enemy_side_card: Union[Card, None] = None, our_side_card_effect: Union[CardEffect, None] = None, enemy_side_card_effect: Union[CardEffect, None] = None) -> bool:
        super_result = super().check_conditon(timing, current_round, our_side_card,
                                              enemy_side_card, our_side_card_effect, enemy_side_card_effect)
        return super_result and timing == self.affect_timing and our_side_card_effect \
            and our_side_card_effect.affect_target == AffectableTarget.ENEMY_SIDE_PLAYER and our_side_card_effect.affect_attribute == AffectableAttribute.SHIELD \
            and our_side_card_effect.affect_operation == AffectableOperation.REDUCE_INT

    def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int, our_side_card: Union[Card, None] = None, enemy_side_card: Union[Card, None] = None, our_side_card_effect: Union[CardEffect, None] = None, enemy_side_card_effect: Union[CardEffect, None] = None) -> Union['Card', CardEffect, None]:
        super_result = super().do_effect(our_side_player, enemy_side_player, current_round,
                                         our_side_card, enemy_side_card, our_side_card_effect, enemy_side_card_effect)
        if not our_side_card_effect:
            raise TypeError(
                f"Expected an CardEffect for our_side_card_effect, got {type(our_side_card_effect).__name__}")
        our_side_card_effect = super_result
        return get_card_effect(CardEffectCreatingInformation(
            CardEffectCreatingInformation.REDUCE_ENEMY_HP, our_side_card_effect.affect_value, our_side_card_effect.affect_probability))

    def get_creating_information(self):
        return PlayerEffectCreatingInformation(PlayerEffectCreatingInformation.GOOD_AT_TAKE_OFF_SHIRT, self.max_affect_times, self.max_affect_round)

    def __reduce__(self):
        return (get_player_effect, (self.get_creating_information(),))


class ApexPredatorPlayerEffect(PlayerEffect):
    def __init__(self,  max_affect_times: int, max_affect_round: int) -> None:
        super().__init__(AffectableTiming.BEFORE_CARD, max_affect_times, max_affect_round,
                         image.get_image(image.EFFECT_APEX_PREDATOR), image.EFFECT_APEX_PREDATOR, PlayerEffectCreatingInformation.APEX_PREDATOR)

    def check_conditon(self, timing: str, current_round: int, our_side_card: Union[Card, None] = None, enemy_side_card: Union[Card, None] = None, our_side_card_effect: Union[CardEffect, None] = None, enemy_side_card_effect: Union[CardEffect, None] = None) -> bool:
        super_result = super().check_conditon(timing, current_round, our_side_card,
                                              enemy_side_card, our_side_card_effect, enemy_side_card_effect)
        return super_result and timing == self.affect_timing \
            and our_side_card

    def do_effect(self, our_side_player: Player, enemy_side_player: Player, current_round: int, our_side_card: Union[Card, None] = None, enemy_side_card: Union[Card, None] = None, our_side_card_effect: Union[CardEffect, None] = None, enemy_side_card_effect: Union[CardEffect, None] = None) -> Union['Card', CardEffect, None]:
        super_result = super().do_effect(our_side_player, enemy_side_player, current_round,
                                         our_side_card, enemy_side_card, our_side_card_effect, enemy_side_card_effect)
        enemy_side_player.add_hp(-2)
        return super_result

    def __reduce__(self):
        return (get_player_effect, (self.get_creating_information(),))


def get_card_effect(creating_information: CardEffectCreatingInformation) -> CardEffect:
    if creating_information.name == CardEffectCreatingInformation.ADD_PLAYER_HP:
        if not isinstance(creating_information.affect_value, int):
            raise TypeError(
                f"Expected an int for creating_information.affect_value, got {type(creating_information.affect_value).__name__}")
        return AddPlayerHpCardEffect(creating_information.affect_value, creating_information.affect_probability)
    elif creating_information.name == CardEffectCreatingInformation.ADD_PLAYER_SHIELD:
        if not isinstance(creating_information.affect_value, int):
            raise TypeError(
                f"Expected an int for creating_information.affect_value, got {type(creating_information.affect_value).__name__}")
        return AddPlayerShieldCardEffect(creating_information.affect_value, creating_information.affect_probability)
    elif creating_information.name == CardEffectCreatingInformation.ADD_ENEMY_HP:
        if not isinstance(creating_information.affect_value, int):
            raise TypeError(
                f"Expected an int for creating_information.affect_value, got {type(creating_information.affect_value).__name__}")
        return AddEnemyHpCardEffect(creating_information.affect_value, creating_information.affect_probability)
    elif creating_information.name == CardEffectCreatingInformation.ADD_ENEMY_SHIELD:
        if not isinstance(creating_information.affect_value, int):
            raise TypeError(
                f"Expected an int for creating_information.affect_value, got {type(creating_information.affect_value).__name__}")
        return AddEnemyShieldCardEffect(creating_information.affect_value, creating_information.affect_probability)
    elif creating_information.name == CardEffectCreatingInformation.REDUCE_PLAYER_HP:
        if not isinstance(creating_information.affect_value, int):
            raise TypeError(
                f"Expected an int for creating_information.affect_value, got {type(creating_information.affect_value).__name__}")
        return ReducePlayerHpCardEffect(creating_information.affect_value, creating_information.affect_probability)
    elif creating_information.name == CardEffectCreatingInformation.REDUCE_PLAYER_SHIELD:
        if not isinstance(creating_information.affect_value, int):
            raise TypeError(
                f"Expected an int for creating_information.affect_value, got {type(creating_information.affect_value).__name__}")
        return ReducePlayerShieldCardEffect(creating_information.affect_value, creating_information.affect_probability)
    elif creating_information.name == CardEffectCreatingInformation.REDUCE_ENEMY_HP:
        if not isinstance(creating_information.affect_value, int):
            raise TypeError(
                f"Expected an int for creating_information.affect_value, got {type(creating_information.affect_value).__name__}")
        return ReduceEnemyHpCardEffect(creating_information.affect_value, creating_information.affect_probability)
    elif creating_information.name == CardEffectCreatingInformation.REDUCE_ENEMY_SHIELD:
        if not isinstance(creating_information.affect_value, int):
            raise TypeError(
                f"Expected an int for creating_information.affect_value, got {type(creating_information.affect_value).__name__}")
        return ReduceEnemyShieldCardEffect(creating_information.affect_value, creating_information.affect_probability)
    elif creating_information.name == CardEffectCreatingInformation.ADD_PLAYER_ATTACK_CARD:
        card_list = creating_information.affect_value[0]
        index = creating_information.affect_value[1]
        if not (isinstance(card_list, list) and all(isinstance(item, int) for item in card_list)):
            raise TypeError(
                f"Expected an List[int] for creating_information.affect_value[0], which is card_id_list, got {type(card_list).__name__}")
        if not isinstance(index, int):
            raise TypeError(
                f"Expected an int for creating_information.affect_value[1], which is index, got {type(index).__name__}")
        return AddPlayerAttackCardCardEffect(creating_information.affect_value, creating_information.affect_probability)
    elif creating_information.name == CardEffectCreatingInformation.ADD_PLAYER_REMAIN_CARD:
        card_list = creating_information.affect_value[0]
        index = creating_information.affect_value[1]
        if not (isinstance(card_list, list) and all(isinstance(item, int) for item in card_list)):
            raise TypeError(
                f"Expected an List[int] for creating_information.affect_value[0], which is card_id_list, got {type(card_list).__name__}")
        if not isinstance(index, int):
            raise TypeError(
                f"Expected an int for creating_information.affect_value[1], which is index, got {type(index).__name__}")
        return AddPlayerRemainCardCardEffect(creating_information.affect_value, creating_information.affect_probability)
    elif creating_information.name == CardEffectCreatingInformation.ADD_ENEMY_ATTACK_CARD:
        card_list = creating_information.affect_value[0]
        index = creating_information.affect_value[1]
        if not (isinstance(card_list, list) and all(isinstance(item, int) for item in card_list)):
            raise TypeError(
                f"Expected an List[int] for creating_information.affect_value[0], which is card_id_list, got {type(card_list).__name__}")
        if not isinstance(index, int):
            raise TypeError(
                f"Expected an int for creating_information.affect_value[1], which is index, got {type(index).__name__}")
        return AddEnemyAttackCardCardEffect(creating_information.affect_value, creating_information.affect_probability)
    elif creating_information.name == CardEffectCreatingInformation.ADD_ENEMY_REMAIN_CARD:
        card_list = creating_information.affect_value[0]
        index = creating_information.affect_value[1]
        if not (isinstance(card_list, list) and all(isinstance(item, int) for item in card_list)):
            raise TypeError(
                f"Expected an List[int] for creating_information.affect_value[0], which is card_id_list, got {type(card_list).__name__}")
        if not isinstance(index, int):
            raise TypeError(
                f"Expected an int for creating_information.affect_value[1], which is index, got {type(index).__name__}")
        return AddEnemyRemainCardCardEffect(creating_information.affect_value, creating_information.affect_probability)
    elif creating_information.name == CardEffectCreatingInformation.ADD_PLAYER_EFFECT_TO_PLAYER:
        if not isinstance(creating_information.affect_value, PlayerEffectCreatingInformation):
            raise TypeError(
                f"Expected an PlayerEffectCreatingInformation for creating_information.affect_value, got {type(creating_information.affect_value).__name__}")
        return AddPlayerEffectToPlayerCardEffect(creating_information.affect_value, creating_information.affect_probability)
    elif creating_information.name == CardEffectCreatingInformation.ADD_PLAYER_EFFECT_TO_ENEMY:
        if not isinstance(creating_information.affect_value, PlayerEffectCreatingInformation):
            raise TypeError(
                f"Expected an PlayerEffectCreatingInformation for creating_information.affect_value, got {type(creating_information.affect_value).__name__}")
        return AddPlayerEffectToEnemyCardEffect(creating_information.affect_value, creating_information.affect_probability)
    raise ValueError(
        f"{creating_information.name} is invalid for creating_information.name")


def get_player_effect(creating_information: PlayerEffectCreatingInformation) -> PlayerEffect:
    if creating_information.name == PlayerEffectCreatingInformation.VOMIT_SUGAR:
        if not isinstance(creating_information.max_round, int):
            raise TypeError(
                f"Expected an int for creating_information.max_round, got {type(creating_information.max_round).__name__}")
        return VomitSugarPlayerEffect(creating_information.max_times, creating_information.max_round)
    elif creating_information.name == PlayerEffectCreatingInformation.FULL_SUGAR:
        if not isinstance(creating_information.max_round, int):
            raise TypeError(
                f"Expected an int for creating_information.max_round, got {type(creating_information.max_round).__name__}")
        return FullSugarPlayerEffect(creating_information.max_times, creating_information.max_round)
    elif creating_information.name == PlayerEffectCreatingInformation.GOOD_AT_TAKE_OFF_SHIRT:
        if not isinstance(creating_information.max_round, int):
            raise TypeError(
                f"Expected an int for creating_information.max_round, got {type(creating_information.max_round).__name__}")
        return GoodAtTakeOffShirtPlayerEffect(creating_information.max_times, creating_information.max_round)
    elif creating_information.name == PlayerEffectCreatingInformation.APEX_PREDATOR:
        if not isinstance(creating_information.max_round, int):
            raise TypeError(
                f"Expected an int for creating_information.max_round, got {type(creating_information.max_round).__name__}")
        return ApexPredatorPlayerEffect(creating_information.max_times, creating_information.max_round)
    raise ValueError(
        f"{creating_information.name} is invalid for creating_information.name")
