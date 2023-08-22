from typing import List
from gui_components import Frame
from game_resource import audio, constants, image
from game_resource.modify_local_data import read_local_card_id_list, read_local_player, write_local_card_id_list, write_local_player, write_local_unlock_player, write_local_unlock_card, read_local_unlock_card, read_local_unlock_player, write_player_creating_information_dict, read_player_creating_information_dict, write_user_point, read_user_point
from pygame import display as pygame_dispaly
import random
from game_element import card_factory, player_factory, PlayerCreatingInformation
from network import Server, Client
from decorator import singleton


@singleton
class Game(Frame):
    _default_player_id: int
    _default_enemy_id: int
    _default_player_card_id_list: List[int]
    _default_all_card_id_list: List[int]
    _default_all_player_id_list: List[int]
    _version: str
    _battle_mode: str
    _server: Server
    _client: Client
    _default_user_point: int

    def __init__(self) -> None:
        bgm_list = [audio.get_bgm(bgm_id) for bgm_id in range(10)]
        random.shuffle(bgm_list)
        super().__init__((constants.WINDOW_WIDTH,
                          constants.WINDOW_HEIGHT), bgm_list)
        pygame_dispaly.set_caption(constants.GAME_TITLE)
        pygame_dispaly.set_icon(image.get_image(image.ICON))
        self._default_player_id = 0
        self._default_enemy_id = 4
        self._default_player_card_id_list = [0, 1, 2, 3, 4,
                                             5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        self._default_all_card_id_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                          11, 12, 13, 14, 15, 16, 600, 601, 602, 603, 604, 605, 606]
        self._default_all_player_id_list = [0, 1, 2, 3, 4, 5]
        self._default_user_point = 0
        self._version = "1.1.0"
        self._battle_mode = None
        self._server = Server()
        self._client = Client()

    def _close(self):
        self._server.close()
        self._client.close()
        return super()._close()

    def get_server(self):
        return self._server

    def get_client(self):
        return self._client

    def set_battle_mode(self, mode: str):
        self._battle_mode = mode

    def get_battle_mode(self):
        return self._battle_mode

    def get_version(self):
        return self._version

    def get_user_point(self):
        read_result = read_user_point()
        if read_result == None:
            return self._default_user_point
        return read_result["point"]

    def add_user_point(self, point: int):
        read_result = read_user_point()
        if read_result == None:
            user_point_dict = {"point": self._default_user_point}
        else:
            user_point_dict = read_result
        user_point_dict["point"] += point
        write_user_point(user_point_dict)

    def get_unlock_card_id_list(self):
        read_result = read_local_unlock_card()
        extra_card_id_list = card_factory.get_all_extra_card_id()
        if read_result == None:
            read_result = [
                card_id for card_id in self._default_all_card_id_list]
        unlock_card_id_list = [
            card_id for card_id in read_result if card_id not in extra_card_id_list]
        unlock_card_id_list.sort()
        return unlock_card_id_list

    def get_unlock_player_id_list(self):
        read_result = read_local_unlock_player()
        if read_result != None:
            unlock_palyer_id_list = [player_id for player_id in read_result]
        else:
            unlock_palyer_id_list = [
                player_id for player_id in self._default_all_player_id_list]
        unlock_palyer_id_list.sort()
        return unlock_palyer_id_list

    def get_player_id(self):
        read_result = read_local_player()
        if read_result != None:
            return read_result
        else:
            return self._default_player_id

    def get_random_enemy_id(self):
        return random.choice(self.get_unlock_player_id_list())

    def get_player_creating_information(self, player_id: int):
        read_result = read_player_creating_information_dict()
        if read_result != None and player_id in read_result.keys():
            return read_result[player_id]
        else:
            return player_factory.get_default_player_creating_information(player_id)

    def set_player_creating_information(self, player_creating_information: PlayerCreatingInformation):
        player_creating_information_dict = read_player_creating_information_dict()
        if player_creating_information_dict != None:
            player_creating_information_dict[player_creating_information.player_id] = player_creating_information
        else:
            player_creating_information_dict = {
                player_creating_information.player_id: player_factory.get_default_player_creating_information(
                    player_creating_information.player_id)}
        write_player_creating_information_dict(
            player_creating_information_dict)

    def get_player_card_id_list(self):
        read_result = read_local_card_id_list()
        if read_result != None:
            player_card_id_list = [card_id for card_id in read_result]
        else:
            player_card_id_list = [
                card_id for card_id in self._default_player_card_id_list]
        player_card_id_list.sort()
        return player_card_id_list

    def get_random_enemy_card_id_list(self):
        all_card_id_list = [
            card_id for card_id in Game().get_unlock_card_id_list()]
        max_result_length = 20
        result_id_list = []
        for _ in range(max_result_length):
            available_card_id_list = [
                card_id for card_id in all_card_id_list if result_id_list.count(card_id) < 2]
            if (not available_card_id_list) or (len(available_card_id_list) == 0):
                break
            selected_card_id = random.choice(available_card_id_list)
            result_id_list.append(selected_card_id)
        result_id_list.sort()
        return result_id_list

    def get_easy_enemy_card_id_list(self):
        return [600, 600, 601, 601, 602, 602, 603, 603, 604, 604, 605, 605]

    def get_normal_enemy_card_id_list(self):
        return [card_id for card_id in self._default_player_card_id_list]

    def set_player_id(self, player_id: int):
        write_local_player(player_id)

    def set_player_card_id_list(self, card_id_list: List[int]):
        card_id_list.sort()
        write_local_card_id_list(card_id_list)

    def add_unlock_card_id(self, card_id: int):
        unlock_card_id_list = read_local_unlock_card()
        if not unlock_card_id_list:
            unlock_card_id_list = [
                card_id for card_id in self._default_all_card_id_list]
            unlock_card_id_list.extend(card_factory.get_all_extra_card_id())
        if card_id not in unlock_card_id_list:
            unlock_card_id_list.append(card_id)
        unlock_card_id_list.sort()
        write_local_unlock_card(unlock_card_id_list)

    def add_unlock_player_id(self, player_id: int):
        unlock_player_id_list = read_local_unlock_player()
        if not unlock_player_id_list:
            unlock_player_id_list = [
                player_id for player_id in self._default_all_player_id_list]
        if player_id not in unlock_player_id_list:
            unlock_player_id_list.append(player_id)
        unlock_player_id_list.sort()
        write_local_unlock_player(unlock_player_id_list)
