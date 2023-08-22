from typing import Any, List, Union


class CardEffectCreatingInformation:
    ADD_PLAYER_HP: str = "add_player_hp"
    ADD_PLAYER_SHIELD: str = "add_player_shield"
    ADD_ENEMY_HP: str = "add_enemy_hp"
    ADD_ENEMY_SHIELD: str = "add_enemy_shield"
    REDUCE_PLAYER_HP: str = "reduce_player_hp"
    REDUCE_PLAYER_SHIELD: str = "reduce_player_shield"
    REDUCE_ENEMY_HP: str = "reduce_enemy_hp"
    REDUCE_ENEMY_SHIELD: str = "reduce_enemy_shield"
    ADD_PLAYER_ATTACK_CARD: str = "add_player_attack_card"
    ADD_PLAYER_REMAIN_CARD: str = "add_player_remain_card"
    ADD_ENEMY_ATTACK_CARD: str = "add_enemy_attack_card"
    ADD_ENEMY_REMAIN_CARD: str = "add_enemy_remain_card"
    ADD_PLAYER_EFFECT_TO_PLAYER: str = "add_player_effect_to_player"
    ADD_PLAYER_EFFECT_TO_ENEMY: str = "add_player_effect_to_enemy"
    name: str
    affect_value: Any
    affect_probability: float

    def __init__(self, name: str, affect_value: Any, affect_probability: float) -> None:
        self.name = name
        self.affect_value = affect_value
        self.affect_probability = affect_probability

    def copy(self):
        return CardEffectCreatingInformation(self.name, self.affect_value, self.affect_probability)

    def __reduce__(self):
        return (self.__class__, (self.name, self.affect_value, self.affect_probability))


class PlayerEffectCreatingInformation:
    VOMIT_SUGAR: str = "vomit_sugar"
    FULL_SUGAR: str = "full_sugar"
    GOOD_AT_TAKE_OFF_SHIRT: str = "good_at_take_off_shirt"
    APEX_PREDATOR: str = "apex_predator"

    CURRENT_ROUND: str = "current_round"
    name: str
    max_times: int
    max_round: Union[int, str]

    def __init__(self, name: str, max_times: int, max_round: Union[int, str]) -> None:
        self.name = name
        self.max_times = max_times
        self.max_round = max_round

    def copy(self):
        return PlayerEffectCreatingInformation(self.name, self.max_times, self.max_round)

    def __reduce__(self):
        return (self.__class__, (self.name, self.max_times, self.max_round))


class PlayerCreatingInformation:
    player_id: int
    name: str
    hp: int
    shield: int
    max_hp: int
    max_shield: int
    effect_list: List[PlayerEffectCreatingInformation]
    deck: List[int]

    def __init__(self, player_id: int, name: str, hp: int, shield: int, max_hp: int, max_shield: int, effect_list: List[PlayerEffectCreatingInformation], deck: List[int]) -> None:
        self.player_id = player_id
        self.name = name
        self.hp = hp
        self.shield = shield
        self.max_hp = max_hp
        self.max_shield = max_shield
        self.effect_list = []
        self.effect_list.extend(effect_list)
        self.deck = []
        self.deck.extend(deck)

    def copy(self):
        return PlayerCreatingInformation(self.player_id, self.name, self.hp, self.shield, self.max_hp, self.max_shield, self.effect_list, self.deck)

    def __reduce__(self):
        return (self.__class__, (self.player_id, self.name, self.hp, self.shield, self.max_hp, self.max_shield, self.effect_list, self.deck))
