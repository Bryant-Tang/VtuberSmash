from abc import abstractmethod
import pickle
import socket
from typing import List
from thread_management import ThreadManager

from .communicate_data import CommunicateData


class Client:
    _client_socket: socket.socket
    _registrants: List["ClientRegistrant"]
    _data_list: List[CommunicateData]

    def __init__(self) -> None:
        self.open()
        self._registrants = []
        self._data_list = []
        self.close()

    def open(self):
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close(self):
        try:
            self._client_socket.close()
        except Exception as e:
            print(f"Client Error: {e}")

    def connect_to_server(self, host: str = None, port: int = None):
        if host != None and port != None:
            try:
                self._client_socket.connect((host, port))
                ThreadManager().run_func_as_new_thread(target=self._handle_server_msg)
                print("connect to server")
                for registrant in self._registrants:
                    registrant.on_connect_to_server()
            except Exception as e:
                print(f"Client Error: {e}")
        return self.is_connect()

    def is_connect(self):
        try:
            self._client_socket.getpeername()
            return True
        except Exception:
            return False

    def get_data(self, command: str):
        result_data_index = None
        for i, data in enumerate(self._data_list):
            if data.command == command:
                result_data_index = i
                break
        if result_data_index != None:
            return self._data_list.pop(result_data_index)
        else:
            return None

    def _handle_server_msg(self):
        self._data_list.clear()
        while True:
            try:
                data = pickle.loads(self._client_socket.recv(1024))
                if not data:
                    break
                if not isinstance(data, CommunicateData):
                    print(f"server data is invalid. server data: {data}")
                    continue
                if data.command == CommunicateData.UNDO_START_BATTLE:
                    for existed_data in self._data_list:
                        if existed_data.command == CommunicateData.START_BATTLE:
                            self._data_list.remove(existed_data)
                            break
                else:
                    self._data_list.append(data)
            except Exception as e:
                print(f"Client Error: {e}")
                break

        if self._client_socket != None:
            self._client_socket.close()
        for registrant in self._registrants:
            registrant.on_server_close()
        print("close connect.")

    def send_game_version(self, version: str):
        try:
            self._client_socket.send(pickle.dumps(
                CommunicateData(CommunicateData.GAME_VERSION, version)))
        except Exception as e:
            print(f"Client Error: {e}")

    def send_start_battle(self):
        try:
            self._client_socket.send(pickle.dumps(
                CommunicateData(CommunicateData.START_BATTLE, None)))
        except Exception as e:
            print(f"Client Error: {e}")

    def send_undo_start_battle(self):
        try:
            self._client_socket.send(pickle.dumps(
                CommunicateData(CommunicateData.UNDO_START_BATTLE, None)))
        except Exception as e:
            print(f"Client Error: {e}")

    def send_name(self, name):
        try:
            self._client_socket.send(pickle.dumps(
                CommunicateData(CommunicateData.NAME, name)))
        except Exception as e:
            print(f"Client Error: {e}")

    def send_player_and_deck(self, player, deck):
        try:
            self._client_socket.send(pickle.dumps(
                CommunicateData(CommunicateData.PLAYER_AND_DECK, (player, deck))))
        except Exception as e:
            print(f"Client Error: {e}")

    def send_attack_card_list(self, attack_card_list):
        try:
            self._client_socket.send(pickle.dumps(
                CommunicateData(CommunicateData.ATTACK_DATA, attack_card_list)))
        except Exception as e:
            print(f"Client Error: {e}")

    def register(self, registrant: "ClientRegistrant"):
        if registrant not in self._registrants:
            self._registrants.append(registrant)

    def unregister(self, registrant: "ClientRegistrant"):
        if registrant in self._registrants:
            self._registrants.remove(registrant)


class ClientRegistrant:
    @abstractmethod
    def on_connect_to_server(self):
        pass

    @abstractmethod
    def on_server_close(self):
        pass
