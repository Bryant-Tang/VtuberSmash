import os
from typing import Dict
from pygame.mixer import Sound

from .constants import File as FileName


EFFECT_SELECT_CARD: str = FileName.AUDIO_SELECT_CARD
EFFECT_CARD_ATTACK: str = FileName.AUDIO_CARD_ATTACK

EFFECT_KSP_7414: str = FileName.AUDIO_KSP_7414
EFFECT_CYGNUS_WTF: str = FileName.AUDIO_CYGNUS_WTF
EFFECT_OUMUA_ANGRY: str = FileName.AUDIO_OUMUA_ANGRY
EFFECT_D2_LOVEU: str = FileName.AUDIO_D2_LOVEU
EFFECT_NEMO_CHARM: str = FileName.AUDIO_NEMO_CHARM
EFFECT_SPRINGFISH_DEADGE: str = FileName.AUDIO_SPRINGFISH_DEADGE
EFFECT_LUTRA_ANGRY: str = FileName.AUDIO_LUTRA_ANGRY
EFFECT_15_SHOOT: str = FileName.AUDIO_15_SHOOT
EFFECT_OBEAR_SHUTUP: str = FileName.AUDIO_OBEAR_SHUTUP
EFFECT_RESCUTE_NONEEDPOOP: str = FileName.AUDIO_RESCUTE_NONEEDPOOP
EFFECT_SEKI_5MA: str = FileName.AUDIO_SEKI_5MA
EFFECT_YANHUA_BABY: str = FileName.AUDIO_YANHUA_BABY
EFFECT_QTTSIX_LOVEYANHUA: str = FileName.AUDIO_QTTSIX_LOVEYANHUA
EFFECT_QTTSIXYANHUA_LOVERS: str = FileName.AUDIO_QTTSIXYANHUA_LOVERS
EFFECT_KSEKI_LOVEEACHOTHER: str = FileName.AUDIO_KSEKI_LOVEEACHOTHER
EFFECT_APEX_POPHEALTH: str = FileName.AUDIO_APEX_POPHEALTH
EFFECT_APEX_POPBAT: str = FileName.AUDIO_APEX_POPBAT
EFFECT_APEX_POPPHINIX: str = FileName.AUDIO_APEX_POPPHINIX
EFFECT_JONGIE_BOMBOMBITCH: str = FileName.AUDIO_JONGIE_BOMBOMBITCH
EFFECT_REN_BEIDOL: str = FileName.AUDIO_REN_BEIDOL
EFFECT_RESTIA_PAYTHEPRICE: str = FileName.AUDIO_RESTIA_PAYTHEPRICE
EFFECT_MARGARET_UNBUTTON: str = FileName.AUDIO_MARGARET_UNBUTTON
EFFECT_LINGLAN_DARKCUISINE: str = FileName.AUDIO_LINGLAN_DARKCUISINE
EFFECT_LINGLAN_WOOFWOOF: str = FileName.AUDIO_LINGLAN_WOOFWOOF
EFFECT_RC_YOUAREGOOD: str = FileName.AUDIO_RC_YOUAREGOOD
EFFECT_RC_WATERMELONMILK: str = FileName.AUDIO_RC_WATERMELONMILK
EFFECT_RSD2_RE45YEAH: str = FileName.AUDIO_RSD2_RE45YEAH
EFFECT_MARGARET_AHHHHH: str = FileName.AUDIO_MARGARET_AHHHHH
EFFECT_EMOTIONAL_DAMAGE: str = FileName.AUDIO_EMOTIONAL_DAMAGE

EFFECT_WINING: str = FileName.AUDIO_WINING
EFFECT_LOSING: str = FileName.AUDIO_LOSING
EFFECT_BTN_DOWN: str = FileName.AUDIO_BTN_DOWN
EFFECT_BTN_UP: str = FileName.AUDIO_BTN_UP
EFFECT_DRAW_CARD_BEGIN: str = FileName.AUDIO_DRAW_CARD_BEGIN
EFFECT_DRAW_CARD: str = FileName.AUDIO_DRAW_CARD

_loaded_sounds: Dict[str, Sound] = {}


def get_sound(sound_name: str) -> Sound:
    global _loaded_sounds
    if sound_name not in _loaded_sounds:
        _loaded_sounds[sound_name] = Sound(
            os.path.join(FileName.FOLDER_ASSET, FileName.FOLDER_AUDIO, sound_name))
    return _loaded_sounds[sound_name]


def get_bgm(bgm_id: int):
    return get_sound(f"bgm_{str(bgm_id).zfill(3)}.mp3")
