from abc import abstractmethod
import random
from typing import Any, Dict, List, Tuple, Union


class AffectableTarget:
    OUR_SIDE_PLAYER = "our_side_player"
    ENEMY_SIDE_PLAYER = "enemy_side_player"


class AffectableAttribute:
    HP = "hp"
    SHIELD = "shield"
    ATTACK_CARD_LIST = "player_attack_card_list"
    REMAIN_CARD_LIST = "player_remain_card_list"
    EFFECT_LIST = "effect_list"


class AffectableOperation:
    ADD_CARD = "add_card"
    REMOVE_CARD = "remove_card"
    ADD_INT = "add_int"
    REDUCE_INT = "reduce_int"
    ADD_EFFECT = "add_effect"
    REMOVE_EFFECT = "remove_effect"


class AffectableTiming:
    BEFORE_ROUND = "before_round"
    BEFORE_CARD = "before_card"
    BEFORE_CARD_EFFECT = "before_card_effect"
    AFTER_CARD_EFFECT = "after_card_effect"
    AFTER_CARD = "after_card"
    AFTER_ROUND = "after_round"
    PERFORM_CARD_ATTACK = "perform_card_attack"


class CardEffect:
    affect_target: str
    affect_attribute: str
    affect_operation: str
    affect_timing: str
    affect_value: Any
    affect_probability: float

    def __init__(self,  affect_target: str, affect_attribute: str, affect_operation: str, affect_timing: str, affect_value: Any, affect_probability: float) -> None:
        self.affect_target = affect_target
        self.affect_attribute = affect_attribute
        self.affect_operation = affect_operation
        self.affect_timing = affect_timing
        self.affect_value = affect_value
        self.affect_probability = affect_probability

    @abstractmethod
    def check_conditon(self, timing: str, current_round: int) -> bool:
        return True

    @abstractmethod
    def do_effect(self, our_side_player: 'Player', enemy_side_player: 'Player', current_round: int):
        pass


class PlayerEffect:
    affect_timing: str
    max_affect_times: int
    max_affect_round: int
    affect_times: int

    def __init__(self, affect_timing: str, max_affect_times: int, max_affect_round: int) -> None:
        self.affect_timing = affect_timing
        self.max_affect_times = max_affect_times
        self.max_affect_round = max_affect_round
        self.affect_times = 0

    def check_fail(self, current_round: int):
        if (current_round > self.max_affect_round) or (self.affect_times >= self.max_affect_times):
            return True
        return False

    @abstractmethod
    def check_conditon(self, timing: str, current_round: int, our_side_card: Union['Card', None] = None, enemy_side_card: Union['Card', None] = None, our_side_card_effect: Union[CardEffect, None] = None, enemy_side_card_effect: Union[CardEffect, None] = None) -> bool:
        if self.check_fail(current_round):
            return False
        return True

    @abstractmethod
    def do_effect(self, our_side_player: 'Player', enemy_side_player: 'Player', current_round: int, our_side_card: Union['Card', None] = None, enemy_side_card: Union['Card', None] = None, our_side_card_effect: Union[CardEffect, None] = None, enemy_side_card_effect: Union[CardEffect, None] = None) -> Union['Card', CardEffect, None]:
        self.affect_times += 1
        has_card = our_side_card or enemy_side_card
        has_card_effect = our_side_card_effect or enemy_side_card_effect
        if has_card and has_card_effect:
            raise ValueError(f"Expected one card or card_effect, not both")
        if our_side_card:
            return our_side_card
        elif enemy_side_card:
            return enemy_side_card
        elif our_side_card_effect:
            return our_side_card_effect
        elif enemy_side_card_effect:
            return enemy_side_card_effect
        else:
            return None


class Card:
    effect_list: List[CardEffect]

    def __init__(self, effect_list: List[CardEffect]) -> None:
        self.effect_list = []
        self.effect_list.extend(effect_list)


class PlayerAttributeRecord:
    hp: int
    shield: int
    max_hp: int
    max_shield: int

    def __init__(self, hp: int, shield: int, max_hp: int, max_shield: int) -> None:
        self.hp = hp
        self.shield = shield
        self.max_hp = max_hp
        self.max_shield = max_shield

    def __reduce__(self):
        return (self.__class__, (self.hp, self.shield, self.max_hp, self.max_shield))


class Player:
    hp: int
    shield: int
    max_hp: int
    max_shield: int
    card_effect_list: List[CardEffect]
    player_effect_list: List[PlayerEffect]
    deck: List[Card]
    attack_card_list: List[Card]
    drawn_card_list: List[Card]

    def __init__(self, hp: int, shield: int, max_hp: int, max_shield: int, player_effect_list: List[PlayerEffect] = [], deck: List[Card] = []) -> None:
        self.hp = hp
        self.shield = shield
        self.max_hp = max_hp
        self.max_shield = max_shield
        self.card_effect_list = []
        self.player_effect_list = []
        self.player_effect_list.extend(player_effect_list)
        self.deck = []
        self.deck.extend(deck)
        self.attack_card_list = []
        self.drawn_card_list = []

    def add_hp(self, value: int):
        self.hp += value
        self.hp = min(self.hp, self.max_hp)
        return self.hp

    def add_shield(self, value: int):
        self.shield += value
        self.shield = min(self.shield, self.max_shield)
        if self.shield < 0:
            self.add_hp(self.shield)
            self.shield = 0
        return self.shield

    def add_attack_card(self, card: Card, index: int = -1):
        self.attack_card_list.insert(index, card)
        return True

    def add_remain_card(self, card: Card, index: int = -1):
        if len(self.drawn_card_list) < 8:
            self.drawn_card_list.insert(index, card)
            return True
        else:
            return False

    def remove_attack_card(self, card: Card):
        if card in self.attack_card_list:
            self.attack_card_list.remove(card)
            return True
        return False

    def remove_remain_card(self, card: Card):
        if card in self.drawn_card_list:
            self.drawn_card_list.remove(card)
            return True
        return False


class ChooseCard:
    player: Player
    enemy: Player

    def __init__(self, player: Player, enemy: Player) -> None:
        self.player = player
        self.enemy = enemy

    def do_draw_card(self, current_round: int):
        '''
        draw cards

        Returns
        ---
        player_drawn_card_list, enemy_drawn_card_list, player_discard_card_list, enemy_discard_card_list
        '''
        player_discard_card_list: List[Card] = []
        enemy_discard_card_list: List[Card] = []
        if current_round == 1:
            for _ in range(2):
                if len(self.player.deck) > 0:
                    draw_card = random.choice(self.player.deck)
                    self.player.drawn_card_list.append(draw_card)
                    self.player.deck.remove(draw_card)
                if len(self.enemy.deck) > 0:
                    draw_card = random.choice(self.enemy.deck)
                    self.enemy.drawn_card_list.append(draw_card)
                    self.enemy.deck.remove(draw_card)
        for _ in range(current_round):
            if len(self.player.deck) > 0:
                draw_card = random.choice(self.player.deck)
                self.player.drawn_card_list.append(draw_card)
                self.player.deck.remove(draw_card)
            if len(self.enemy.deck) > 0:
                draw_card = random.choice(self.enemy.deck)
                self.enemy.drawn_card_list.append(draw_card)
                self.enemy.deck.remove(draw_card)

        while len(self.player.drawn_card_list) > 8:
            player_discard_card_list.append(self.player.drawn_card_list.pop())
        while len(self.enemy.drawn_card_list) > 8:
            enemy_discard_card_list.append(self.enemy.drawn_card_list.pop())

        return self.player.drawn_card_list, self.enemy.drawn_card_list, player_discard_card_list, enemy_discard_card_list

    def set_attack_card(self, our_side_player_attack_card_list: List[Card], enemy_side_player_attack_card_list: List[Card], current_round: int):
        '''
        set the attack card for our_side_player and enemy_side_player

        Returns
        ---
        Player, Player
            the player and enemy respectively after setting attack card
        '''
        if len(our_side_player_attack_card_list) > current_round:
            return False
        for card in our_side_player_attack_card_list:
            if card in self.player.drawn_card_list:
                self.player.drawn_card_list.remove(card)
            self.player.attack_card_list.append(card)
        for card in enemy_side_player_attack_card_list:
            if card in self.enemy.drawn_card_list:
                self.enemy.drawn_card_list.remove(card)
            self.enemy.attack_card_list.append(card)
        return self.player, self.enemy


class Battle:
    player: Player
    enemy: Player

    def __init__(self, player: Player, enemy: Player) -> None:
        self.player = player
        self.enemy = enemy

    def perform_round(self, current_round: int):
        '''
        perform a round

        Returns
        ---
        winner, operation_record, attribute_record
            winner: Player if has winner else None
            operation_record: {
                "round_start": round_start_result,
                f"attacked_card_result_{i}": perform_card_result,
                "round_end": round_end_result
            }
                round_xxx_result: Tuple[None, None, activated_player_effect_list: List[PlayerEffect], removed_player_effect: List[PlayerEffect]]

                perform_card_result: Tuple[attack_card: Card, activated_card_effect_list: List[CardEffect], activated_player_effect_list: List[PlayerEffect], removed_player_effect: List[PlayerEffect]]

            attribute_record: List[
                initial_attribute_record,
                round_start_effect_attribute_record,
                f"attacked_card_result_{i}__attribute_record",
                round_end_effect_attribute_record]
        '''
        operation_record: Dict[str, Tuple[Union[Card, None],
                                          Union[List[CardEffect], None], List[PlayerEffect], List[PlayerEffect]]] = {}
        attribute_record: List[Tuple[PlayerAttributeRecord,
                                     PlayerAttributeRecord]] = []
        winner, attribute = self._check_player_attribute()
        attribute_record.append(attribute)
        if winner:
            return winner, operation_record, attribute_record

        round_start_removed_effect_list, round_start_effect_list\
            = self._round_start(current_round)
        operation_record["round_start"] = (
            None, None, round_start_effect_list, round_start_removed_effect_list)
        winner, attribute = self._check_player_attribute()
        attribute_record.append(attribute)
        if winner:
            return winner, operation_record, attribute_record

        i = 0
        while True:
            perform_card_result = self._perform_one_card(current_round)
            if not perform_card_result:
                break
            operation_record[f"attacked_card_result_{i}"] = perform_card_result
            winner, attribute = self._check_player_attribute()
            attribute_record.append(attribute)
            if winner:
                return winner, operation_record, attribute_record
            i += 1

        round_end_effect_list, round_end_removed_effect_list\
            = self._round_end(current_round)
        operation_record["round_end"] = (
            None, None, round_end_effect_list, round_end_removed_effect_list)
        winner, attribute = self._check_player_attribute()
        attribute_record.append(attribute)
        if winner:
            return winner, operation_record, attribute_record

        return None, operation_record, attribute_record

    def _check_player_attribute(self) -> Tuple[Player, Tuple[PlayerAttributeRecord, PlayerAttributeRecord]]:
        player_attribute = PlayerAttributeRecord(
            self.player.hp, self.player.shield, self.player.max_hp, self.player.max_shield)
        enemy_attribute = PlayerAttributeRecord(
            self.enemy.hp, self.enemy.shield, self.enemy.max_hp, self.enemy.max_shield)
        if player_attribute.hp <= 0:
            return self.enemy, (player_attribute, enemy_attribute)
        elif enemy_attribute.hp <= 0:
            return self.player, (player_attribute, enemy_attribute)
        else:
            return None, (player_attribute, enemy_attribute)

    def _round_start(self, current_round: int):
        return self._check_player_effect_fail(current_round), self._do_player_effect_before_round(current_round)

    def _perform_one_card(self, current_round: int):
        '''
        perform one card attack

        Returns
        -------
        Literal[False] |
        tuple[Card, list[CardEffect], list[PlayerEffect], list[PlayerEffect]]

            return attacked_card, activated_card_effect_list, activated_player_effect_list, removed_player_effect

            if result is False means there is no card to attack
        '''
        # get one attack card
        card: Card
        card_belong_local_player: bool
        activated_player_effect_list: List[PlayerEffect] = []
        activated_card_effect_list: List[CardEffect] = []

        if (len(self.player.attack_card_list) > 0) and (len(self.enemy.attack_card_list) > 0):
            chosen_player = random.choice([self.player, self.enemy])
            if chosen_player is self.player:
                card_belong_local_player = True
            else:
                card_belong_local_player = False
            card = chosen_player.attack_card_list.pop(0)
        elif len(self.player.attack_card_list) > 0:
            card = self.player.attack_card_list.pop(0)
            card_belong_local_player = True
        elif len(self.enemy.attack_card_list) > 0:
            card = self.enemy.attack_card_list.pop(0)
            card_belong_local_player = False
        else:
            return False

        # do before card effect
        card, this_step_activated_player_effect_list = self._do_player_effect_before_card(
            card, card_belong_local_player, current_round)
        activated_player_effect_list.extend(
            this_step_activated_player_effect_list)

        # set player card effect list
        if card_belong_local_player:
            self.player.card_effect_list.clear()
            self.player.card_effect_list.extend(card.effect_list)
        else:
            self.enemy.card_effect_list.clear()
            self.enemy.card_effect_list.extend(card.effect_list)

        # perform one card attack
        while True:
            if card_belong_local_player:
                if len(self.player.card_effect_list) == 0:
                    break
                else:
                    card_effect = self.player.card_effect_list.pop(0)
            else:
                if len(self.enemy.card_effect_list) == 0:
                    break
                else:
                    card_effect = self.enemy.card_effect_list.pop(0)

            # do before card effect effect
            card_effect, this_step_activated_player_effect_list = self._do_player_effect_before_card_effect(
                card_effect, card_belong_local_player, current_round)
            activated_player_effect_list.extend(
                this_step_activated_player_effect_list)

            # do one card effect
            if random.random() < card_effect.affect_probability:
                if card_belong_local_player:
                    card_effect.do_effect(
                        self.player, self.enemy, current_round)
                else:
                    card_effect.do_effect(
                        self.enemy, self.player, current_round)
                activated_card_effect_list.append(card_effect)

            # do after card effect effect
            activated_player_effect_list.extend(
                self._do_player_effect_after_card_effect(card_effect, card_belong_local_player, current_round))

        # do after card effect
        activated_player_effect_list.extend(
            self._do_player_effect_after_card(card, card_belong_local_player, current_round))

        removed_player_effect = self._check_player_effect_fail(current_round)

        return card, activated_card_effect_list, activated_player_effect_list, removed_player_effect

    def _round_end(self, current_round: int):
        return self._do_player_effect_after_round(current_round), self._check_player_effect_fail(current_round)

    def _check_player_effect_fail(self, current_round: int):
        removed_effect: List[PlayerEffect] = []
        for player_effect in self.player.player_effect_list:
            if player_effect.check_fail(current_round):
                self.player.player_effect_list.remove(player_effect)
                removed_effect.append(player_effect)
        for player_effect in self.enemy.player_effect_list:
            if player_effect.check_fail(current_round):
                self.enemy.player_effect_list.remove(player_effect)
                removed_effect.append(player_effect)
        return removed_effect

    def _do_player_effect_before_round(self, current_round: int):
        activated_player_effect: List[PlayerEffect] = []
        for player_effect in self.player.player_effect_list:
            if player_effect.check_conditon(AffectableTiming.BEFORE_ROUND, current_round):
                player_effect.do_effect(self.player, self.enemy, current_round)
                activated_player_effect.append(player_effect)
        for player_effect in self.enemy.player_effect_list:
            if player_effect.check_conditon(AffectableTiming.BEFORE_ROUND, current_round):
                player_effect.do_effect(self.enemy, self.player, current_round)
                activated_player_effect.append(player_effect)
        return activated_player_effect

    def _do_player_effect_before_card(self, card: Card, card_belong_local_player: bool, current_round: int):
        activated_player_effect: List[PlayerEffect] = []
        for player_effect in self.player.player_effect_list:
            if card_belong_local_player:
                if player_effect.check_conditon(AffectableTiming.BEFORE_CARD, current_round, our_side_card=card):
                    result = player_effect.do_effect(
                        self.player, self.enemy, current_round, our_side_card=card)
                    if isinstance(result, Card):
                        card = result
                    activated_player_effect.append(player_effect)
            else:
                if player_effect.check_conditon(AffectableTiming.BEFORE_CARD, current_round, enemy_side_card=card):
                    result = player_effect.do_effect(
                        self.player, self.enemy, current_round, enemy_side_card=card)
                    if isinstance(result, Card):
                        card = result
                    activated_player_effect.append(player_effect)
        for player_effect in self.enemy.player_effect_list:
            if card_belong_local_player:
                if player_effect.check_conditon(AffectableTiming.BEFORE_CARD, current_round, enemy_side_card=card):
                    result = player_effect.do_effect(
                        self.player, self.enemy, current_round, enemy_side_card=card)
                    if isinstance(result, Card):
                        card = result
                    activated_player_effect.append(player_effect)
            else:
                if player_effect.check_conditon(AffectableTiming.BEFORE_CARD, current_round, our_side_card=card):
                    result = player_effect.do_effect(
                        self.player, self.enemy, current_round, our_side_card=card)
                    if isinstance(result, Card):
                        card = result
                    activated_player_effect.append(player_effect)
        return card, activated_player_effect

    def _do_player_effect_before_card_effect(self, card_effect: CardEffect, card_effect_belong_local_player: bool, current_round: int):
        activated_player_effect: List[PlayerEffect] = []
        for player_effect in self.player.player_effect_list:
            if card_effect_belong_local_player:
                if player_effect.check_conditon(AffectableTiming.BEFORE_CARD_EFFECT, current_round, our_side_card_effect=card_effect):
                    result = player_effect.do_effect(self.player, self.enemy,
                                                     current_round, our_side_card_effect=card_effect)
                    if isinstance(result, CardEffect):
                        card_effect = result
                    activated_player_effect.append(player_effect)
            else:
                if player_effect.check_conditon(AffectableTiming.BEFORE_CARD_EFFECT, current_round, enemy_side_card_effect=card_effect):
                    result = player_effect.do_effect(self.player, self.enemy,
                                                     current_round, enemy_side_card_effect=card_effect)
                    if isinstance(result, CardEffect):
                        card_effect = result
                    activated_player_effect.append(player_effect)

        for player_effect in self.enemy.player_effect_list:
            if card_effect_belong_local_player:
                if player_effect.check_conditon(AffectableTiming.BEFORE_CARD_EFFECT, current_round, enemy_side_card_effect=card_effect):
                    result = player_effect.do_effect(self.enemy, self.player, current_round,
                                                     enemy_side_card_effect=card_effect)
                    if isinstance(result, CardEffect):
                        card_effect = result
                    activated_player_effect.append(player_effect)
            else:
                if player_effect.check_conditon(AffectableTiming.BEFORE_CARD_EFFECT, current_round, our_side_card_effect=card_effect):
                    result = player_effect.do_effect(self.enemy, self.player, current_round,
                                                     our_side_card_effect=card_effect)
                    if isinstance(result, CardEffect):
                        card_effect = result
                    activated_player_effect.append(player_effect)
        return card_effect, activated_player_effect

    def _do_player_effect_after_card_effect(self, card_effect: CardEffect, card_effect_belong_local_player: bool, current_round: int):
        activated_player_effect: List[PlayerEffect] = []
        for player_effect in self.player.player_effect_list:
            if card_effect_belong_local_player:
                if player_effect.check_conditon(AffectableTiming.AFTER_CARD_EFFECT, current_round, our_side_card_effect=card_effect):
                    player_effect.do_effect(self.player, self.enemy,
                                            current_round, our_side_card_effect=card_effect)
                    activated_player_effect.append(player_effect)
            else:
                if player_effect.check_conditon(AffectableTiming.AFTER_CARD_EFFECT, current_round, enemy_side_card_effect=card_effect):
                    player_effect.do_effect(self.player, self.enemy,
                                            current_round, enemy_side_card_effect=card_effect)
                    activated_player_effect.append(player_effect)

        for player_effect in self.enemy.player_effect_list:
            if card_effect_belong_local_player:
                if player_effect.check_conditon(AffectableTiming.AFTER_CARD_EFFECT, current_round, enemy_side_card_effect=card_effect):
                    player_effect.do_effect(self.enemy, self.player, current_round,
                                            enemy_side_card_effect=card_effect)
                    activated_player_effect.append(player_effect)
            else:
                if player_effect.check_conditon(AffectableTiming.AFTER_CARD_EFFECT, current_round, our_side_card_effect=card_effect):
                    player_effect.do_effect(self.enemy, self.player, current_round,
                                            our_side_card_effect=card_effect)
                    activated_player_effect.append(player_effect)
        return activated_player_effect

    def _do_player_effect_after_card(self, card: Card, card_belong_local_player: bool, current_round: int):
        activated_player_effect: List[PlayerEffect] = []
        for player_effect in self.player.player_effect_list:
            if card_belong_local_player:
                if player_effect.check_conditon(AffectableTiming.AFTER_CARD, current_round, our_side_card=card):
                    player_effect.do_effect(
                        self.player, self.enemy, current_round, our_side_card=card)
                    activated_player_effect.append(player_effect)
            else:
                if player_effect.check_conditon(AffectableTiming.AFTER_CARD, current_round, enemy_side_card=card):
                    player_effect.do_effect(
                        self.player, self.enemy, current_round, enemy_side_card=card)
                    activated_player_effect.append(player_effect)
        for player_effect in self.enemy.player_effect_list:
            if card_belong_local_player:
                if player_effect.check_conditon(AffectableTiming.AFTER_CARD, current_round, enemy_side_card=card):
                    player_effect.do_effect(
                        self.player, self.enemy, current_round, enemy_side_card=card)
                    activated_player_effect.append(player_effect)
            else:
                if player_effect.check_conditon(AffectableTiming.AFTER_CARD, current_round, our_side_card=card):
                    player_effect.do_effect(
                        self.player, self.enemy, current_round, our_side_card=card)
                    activated_player_effect.append(player_effect)
        return activated_player_effect

    def _do_player_effect_after_round(self, current_round: int):
        activated_player_effect: List[PlayerEffect] = []
        for player_effect in self.player.player_effect_list:
            if player_effect.check_conditon(AffectableTiming.AFTER_ROUND, current_round):
                player_effect.do_effect(self.player, self.enemy, current_round)
                activated_player_effect.append(player_effect)
        for player_effect in self.enemy.player_effect_list:
            if player_effect.check_conditon(AffectableTiming.AFTER_ROUND, current_round):
                player_effect.do_effect(self.enemy, self.player, current_round)
                activated_player_effect.append(player_effect)
        return activated_player_effect
