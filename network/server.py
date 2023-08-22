from abc import abstractmethod
import pickle
import socket
from typing import List, Tuple
from thread_management import ThreadManager

from .communicate_data import CommunicateData


class Server:
    _client_socket: socket.socket
    _server_socket: socket.socket
    _addr: Tuple[str, int]
    _registrants: List["ServerRegistrant"]
    search_client_end: bool
    _data_list: List[CommunicateData]

    def __init__(self):
        self._addr = None
        self.open()
        self._client_socket = None
        self._registrants = []
        self.search_client_end = False
        self._data_list = []
        self.close()

    def open(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close(self):
        try:
            self._server_socket.close()
        except Exception as e:
            print(f"Server Error: {e}")

        try:
            if isinstance(self._client_socket, socket.socket):
                self._client_socket.close()
        except Exception as e:
            print(f"Server Error: {e}")

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

    def start_search_client(self, host: str = None, port: int = None):
        self.search_client_end = False
        if host != None and port != None:
            self._addr = (host, port)
        if self._addr == None:
            print("Server IP is not set.")
            return
        self._server_socket.bind(self._addr)
        self._server_socket.listen()
        print("Server is listening...")
        while True:
            if self.search_client_end:
                break
            try:
                temp_client_socket, _ = self._server_socket.accept()
                if self._client_socket != None:
                    temp_client_socket.send(pickle.dumps(
                        CommunicateData(CommunicateData.SERVER_FULL, None)))
                    temp_client_socket.close()
                else:
                    self._client_socket = temp_client_socket
                    ThreadManager().run_func_as_new_thread(target=self._handle_client_msg)
                    for registrant in self._registrants:
                        registrant.on_new_player_connected()
            except Exception as e:
                print(f"Server Error: {e}")
                break
        print("Server end listening.")

    def _handle_client_msg(self):
        # temp code
        self.search_client_end = True
        self._data_list.clear()

        while True:
            try:
                data = pickle.loads(self._client_socket.recv(1024))
                if (not data):
                    break
                if not isinstance(data, CommunicateData):
                    print(f"client data is invalid. client data: {data}")
                    continue
                if data.command == CommunicateData.UNDO_START_BATTLE:
                    for existed_data in self._data_list:
                        if existed_data.command == CommunicateData.START_BATTLE:
                            self._data_list.remove(existed_data)
                            break
                else:
                    self._data_list.append(data)
            except Exception as e:
                print(f"Server Error: {e}")
                break

        if self._client_socket != None:
            self._client_socket.close()
        self._client_socket = None
        for registrant in self._registrants:
            registrant.on_client_close()
        print("client close.")

    def send_game_version(self, version: str):
        try:
            self._client_socket.send(pickle.dumps(
                CommunicateData(CommunicateData.GAME_VERSION, version)))
        except Exception as e:
            print(f"Server Error: {e}")

    def send_start_battle(self):
        try:
            self._client_socket.send(pickle.dumps(
                CommunicateData(CommunicateData.START_BATTLE, None)))
        except Exception as e:
            print(f"Server Error: {e}")

    def send_undo_start_battle(self):
        try:
            self._client_socket.send(pickle.dumps(
                CommunicateData(CommunicateData.UNDO_START_BATTLE, None)))
        except Exception as e:
            print(f"Server Error: {e}")

    def send_name(self, name):
        try:
            self._client_socket.send(pickle.dumps(
                CommunicateData(CommunicateData.NAME, name)))
        except Exception as e:
            print(f"Server Error: {e}")

    def send_player_and_deck(self, player, deck):
        try:
            self._client_socket.send(pickle.dumps(
                CommunicateData(CommunicateData.PLAYER_AND_DECK, (player, deck))))
        except Exception as e:
            print(f"Server Error: {e}")

    def send_deck_and_drawn_card_list_and_discard_card_list(self, deck, drawn_card_list, discard_card_list):
        try:
            self._client_socket.send(pickle.dumps(
                CommunicateData(CommunicateData.DECK_AND_DRAWN_CARD_AND_DISCARD_CARD, (deck, drawn_card_list, discard_card_list))))
        except Exception as e:
            print(f"Server Error: {e}")

    def send_round_result(self, round_result):
        try:
            self._client_socket.send(pickle.dumps(
                CommunicateData(CommunicateData.ROUND_RESULT, round_result)))
        except Exception as e:
            print(f"Server Error: {e}")

    def register(self, registrant: "ServerRegistrant"):
        if registrant not in self._registrants:
            self._registrants.append(registrant)

    def unregister(self, registrant: "ServerRegistrant"):
        if registrant in self._registrants:
            self._registrants.remove(registrant)


class ServerRegistrant:
    @abstractmethod
    def on_new_player_connected(self):
        pass

    @abstractmethod
    def on_client_close(self):
        pass
