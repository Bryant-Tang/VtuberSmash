from typing import Any, Union
import socket


class CommunicateData:
    GAME_VERSION: str = "game_version"
    SERVER_FULL: str = "server_full"
    START_BATTLE: str = "start_battle"
    UNDO_START_BATTLE: str = "undo_start_battle"
    NAME: str = "name"
    PLAYER_AND_DECK: str = "player_and_deck"
    DECK_AND_DRAWN_CARD_AND_DISCARD_CARD: str = "deck_and_drawn_card_and_discard_card"
    ATTACK_DATA: str = "attack_data"
    ROUND_RESULT: str = "round_result"
    command: str
    data: Any

    def __init__(self, command, data) -> None:
        self.command = command
        self.data = data

    def __reduce__(self):
        return (self.__class__, (self.command, self.data))


def is_valid_ip(ip: str):
    try:
        socket.inet_pton(socket.AF_INET, ip)
        return True
    except socket.error:
        pass

    try:
        socket.inet_pton(socket.AF_INET6, ip)
        return True
    except socket.error:
        return False


def is_valid_port(port: Union[str, int]):
    if isinstance(port, str):
        if port.isdigit():
            port = int(port)
        else:
            return False
    return 1024 <= port and port <= 49151
