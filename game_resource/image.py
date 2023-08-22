import os
from typing import Dict
import pygame
from pygame import Surface, transform as pygame_transform

from .constants import File as FileName, CARD_WIDTH, CARD_HEIGHT

BG_BATTLE_FIELD: str = FileName.IMAGE_BG_BATTLE_FIELD
BG_MENU: str = FileName.IMAGE_BG_MENU
BTN_TEXT_UP: str = FileName.IMAGE_BTN_TEXT_UP
BTN_TEXT_DOWN: str = FileName.IMAGE_BTN_TEXT_DOWN
BTN_TEXT_UP_WIDTH2X: str = FileName.IMAGE_BTN_TEXT_UP_WIDTH2X
BTN_TEXT_DOWN_WIDTH2X: str = FileName.IMAGE_BTN_TEXT_DOWN_WIDTH2X
BTN_LEFT_UP: str = FileName.IMAGE_BTN_LEFT_UP
BTN_LEFT_DOWN: str = FileName.IMAGE_BTN_LEFT_DOWN
BTN_RIGHT_UP: str = FileName.IMAGE_BTN_RIGHT_UP
BTN_RIGHT_DOWN: str = FileName.IMAGE_BTN_RIGHT_DOWN
BATTLE_CARD_ATTACK_BG: str = FileName.IMAGE_BATTLE_CARD_ATTACK_BG
WIN_SIGN: str = FileName.IMAGE_WIN_SIGN
LOSE_SIGN: str = FileName.IMAGE_LOSE_SIGN
ROUND_START_SIGN: str = FileName.IMAGE_ROUND_START_SIGN
ROUND_END_SIGN: str = FileName.IMAGE_ROUND_END_SIGN
PLAYER_HP: str = FileName.IMAGE_PLAYER_HP
PLAYER_SHIELD: str = FileName.IMAGE_PLAYER_SHIELD
PLAYER_HP_BG: str = FileName.IMAGE_PLAYER_HP_BG
PLAYER_SHIELD_BG: str = FileName.IMAGE_PLAYER_SHIELD_BG
EFFECT_VOMIT_SUGAR: str = FileName.IMAGE_EFFECT_VOMIT_SUGAR
EFFECT_FULL_SUGAR: str = FileName.IMAGE_EFFECT_FULL_SUGAR
EFFECT_GOOD_AT_TAKE_OFF_SHIRT: str = FileName.IMAGE_GOOD_AT_TAKE_OFF_SHIRT
EFFECT_APEX_PREDATOR: str = FileName.IMAGE_APEX_PREDATOR
CARD_DISCARD_MASK: str = FileName.IMAGE_CARD_DISCARD_MASK
CARD_LOCK: str = FileName.IMAGE_CARD_LOCK
NOT_FINISH_SIGN: str = FileName.IMAGE_NOT_FINISH_SIGN
MODE_DETAIL_EASY: str = FileName.IMAGE_MODE_DETAIL_EASY
MODE_DETAIL_NORMAL: str = FileName.IMAGE_MODE_DETAIL_NORMAL
MODE_DETAIL_HARD: str = FileName.IMAGE_MODE_DETAIL_HARD
MODE_DETAIL_SUPER_HARD: str = FileName.IMAGE_MODE_DETAIL_SUPER_HARD
MODE_DETAIL_ASIAN: str = FileName.IMAGE_MODE_DETAIL_ASIAN
MODE_DETAIL_RANDOM: str = FileName.IMAGE_MODE_DETAIL_RANDOM
MODE_DETAIL_CREATE_CONNECT: str = FileName.IMAGE_MODE_DETAIL_CREATE_CONNECT
MODE_DETAIL_JOIN_CONNECT: str = FileName.IMAGE_MODE_DETAIL_JOIN_CONNECT

ICON: str = FileName.IMAGE_ICON
GAME_RULE_0: str = FileName.IMAGE_GAME_RULE_0
GAME_RULE_1: str = FileName.IMAGE_GAME_RULE_1
GAME_RULE_2: str = FileName.IMAGE_GAME_RULE_2
GAME_RULE_3: str = FileName.IMAGE_GAME_RULE_3
GAME_RULE_4: str = FileName.IMAGE_GAME_RULE_4
DECLARATION_ZH: str = FileName.IMAGE_DECLARATION_ZH
DECLARATION_EN: str = FileName.IMAGE_DECLARATION_EN
ABOUT_GAME_00: str = FileName.IMAGE_ABOUT_GAME_00
ABOUT_GAME_01: str = FileName.IMAGE_ABOUT_GAME_01
ABOUT_GAME_02: str = FileName.IMAGE_ABOUT_GAME_02
ABOUT_GAME_03: str = FileName.IMAGE_ABOUT_GAME_03
GACHA_POOL_BASEPLAYER: str = FileName.IMAGE_GACHA_POOL_BASEPLAYER
GACHA_POOL_DETAIL_BASEPLAYER: str = FileName.IMAGE_GACHA_POOL_DETAIL_BASEPLAYER

_loaded_images: Dict[str, Surface] = {}


def get_image(image_name: str) -> Surface:
    global _loaded_images
    if image_name not in _loaded_images:
        _loaded_images[image_name] = pygame.image.load(
            os.path.join(FileName.FOLDER_ASSET, FileName.FOLDER_IMAGE, image_name))
    return _loaded_images[image_name].copy()


def card(card_id: int) -> Surface:
    if card_id == 1000:
        card_img = get_image(f"card_1000.png")
    else:
        card_img = get_image(f"card_{str(card_id).zfill(3)}.png")
    card_img = pygame_transform.scale(card_img, (CARD_WIDTH, CARD_HEIGHT))
    return card_img


def get_card_file_name(card_id: int):
    return f"card_{str(card_id).zfill(3)}.png"


def card_detail(card_id: int) -> Surface:
    return get_image(f"card_detail_{str(card_id).zfill(3)}.png")


def player(player_id: int) -> Surface:
    return get_image(f"player_{str(player_id).zfill(3)}.png")


def player_detail(player_id: int) -> Surface:
    return get_image(f"player_detail_{str(player_id).zfill(3)}.png")


def player_fullbody(player_id: int) -> Surface:
    return get_image(f"player_fullbody_{str(player_id).zfill(3)}.png")


def player_effect_handbook(page_id: int) -> Surface:
    return get_image(f"player_effect_handbook_{str(page_id).zfill(3)}.png")
