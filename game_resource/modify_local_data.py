from typing import Any, Dict, List, Union
import os
import struct
import pickle
from game_element import PlayerCreatingInformation
from .constants import File as FileName


def write_local_player(player_id: int):
    _write_int_list_to_file(FileName.FOLDER_LOCAL_DATA, "player", [player_id])


def write_local_card_id_list(card_id_list: List[int]):
    _write_int_list_to_file(FileName.FOLDER_LOCAL_DATA, "card", card_id_list)


def write_local_unlock_player(player_id_list: List[int]):
    _write_int_list_to_file(FileName.FOLDER_LOCAL_DATA,
                            "unlock_player", player_id_list)


def write_local_unlock_card(card_id_list: List[int]):
    _write_int_list_to_file(FileName.FOLDER_LOCAL_DATA,
                            "unlock_card", card_id_list)


def write_player_creating_information_dict(player_creating_information_dict: Dict[int, PlayerCreatingInformation]):
    _write_custom_class_to_file(FileName.FOLDER_LOCAL_DATA,
                                "player_creating_information", player_creating_information_dict)


def write_user_point(user_point_dict: Dict[str, int]):
    _write_custom_class_to_file(FileName.FOLDER_LOCAL_DATA,
                                "user_point", user_point_dict)


def read_user_point() -> Union[Dict[str, int], None]:
    result = _read_custom_class_from_file(
        FileName.FOLDER_LOCAL_DATA, "user_point")
    if result == None:
        return result
    if not (isinstance(result, Dict) and all(isinstance(key, str)
                                             and isinstance(value, int) for key, value in result.items())):
        raise ValueError(
            "The local user point file content is invalid.")
    return result


def read_player_creating_information_dict() -> Union[Dict[int, PlayerCreatingInformation], None]:
    result = _read_custom_class_from_file(
        FileName.FOLDER_LOCAL_DATA, "player_creating_information")
    if result == None:
        return result
    if not (isinstance(result, Dict) and all(isinstance(key, int)
                                             and isinstance(value, PlayerCreatingInformation) for key, value in result.items())):
        raise ValueError(
            "The local player creating information file content is invalid.")
    return result


def read_local_player():
    result = _read_int_list_from_file(FileName.FOLDER_LOCAL_DATA, "player")
    if result == None:
        return result
    if not (isinstance(result, list) and len(result) > 0 and all(isinstance(card_id, int) for card_id in result)):
        raise ValueError("The local player file content is invalid.")
    return result[0]


def read_local_card_id_list():
    result = _read_int_list_from_file(FileName.FOLDER_LOCAL_DATA, "card")
    if result == None:
        return result
    if not (isinstance(result, list) and all(isinstance(card_id, int) for card_id in result)):
        raise ValueError("The local card file content is invalid.")
    return result


def read_local_unlock_player():
    result = _read_int_list_from_file(
        FileName.FOLDER_LOCAL_DATA, "unlock_player")
    if result == None:
        return result
    if not (isinstance(result, list) and all(isinstance(player_id, int) for player_id in result)):
        raise ValueError("The local unlock_player file content is invalid.")
    return result


def read_local_unlock_card():
    result = _read_int_list_from_file(
        FileName.FOLDER_LOCAL_DATA, "unlock_card")
    if result == None:
        return result
    if not (isinstance(result, list) and all(isinstance(card_id, int) for card_id in result)):
        raise ValueError("The local unlock_card file content is invalid.")
    return result


def _write_custom_class_to_file(folder_name: str, file_name: str, data: Any) -> str:
    binary_data = pickle.dumps(data)

    appdata_path = os.path.join(os.environ["APPDATA"], folder_name)
    os.makedirs(appdata_path, exist_ok=True)
    file_path = os.path.join(appdata_path, file_name + ".bin")

    with open(file_path, "wb") as file:
        file.write(binary_data)

    return file_path


def _read_custom_class_from_file(folder_name: str, file_name: str) -> Any:
    appdata_path = os.path.join(os.environ["APPDATA"], folder_name)
    file_path = os.path.join(appdata_path, file_name + ".bin")

    if not os.path.exists(file_path):
        return None

    with open(file_path, "rb") as file:
        binary_data = file.read()

    result = pickle.loads(binary_data)

    return result


def _write_int_list_to_file(folder_name: str, file_name: str, data: List[int]) -> str:
    binary_data = struct.pack("i" * len(data), *data)

    appdata_path = os.path.join(os.environ["APPDATA"], folder_name)
    os.makedirs(appdata_path, exist_ok=True)
    file_path = os.path.join(appdata_path, file_name + ".bin")

    with open(file_path, "wb") as file:
        file.write(binary_data)

    return file_path


def _read_int_list_from_file(folder_name: str, file_name: str) -> Union[List[int], None]:
    appdata_path = os.path.join(os.environ["APPDATA"], folder_name)
    file_path = os.path.join(appdata_path, file_name + ".bin")

    if not os.path.exists(file_path):
        return None

    with open(file_path, "rb") as file:
        binary_data = file.read()

    int_list = list(struct.unpack(
        "i" * (len(binary_data) // 4), binary_data))

    return int_list
