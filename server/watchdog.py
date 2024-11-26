import threading
import signal
import os

SERVER_HOST = "localhost"
SERVER_PORT = 1111

global _all_addresses
global _active_address
global _active_player
global _player1_name
global _player2_name
global _player_name

class Watchdog:

    def __init__(self, timeout=10):
        self.timeout = timeout
        self._t = None

    def set_addresses(self, address1: tuple, address2: tuple):
        global _all_addresses
        _all_addresses = [tuple(address1), tuple(address2)]

    def set_names(self, player1_name, player2_name):
        global _player1_name
        global _player2_name

        _player1_name = player1_name
        _player2_name = player2_name

    def get_names(self):
        return [_player1_name, _player2_name]

    @staticmethod
    def get_addresses():
        return _all_addresses

    @staticmethod
    def set_player(addr, player_name):
        global _player_name
        _player_name = player_name

        global _active_player
        global _active_address
        if addr == _all_addresses[0]:
            _active_player = 1
            _active_address = _all_addresses[0]
        else:
            _active_player = 2
            _active_address = _all_addresses[1]

    def _expire(self):
        from server import send_all
        from server import send_msg

        send_all(f"Partida Encerrada, Jogador P{_active_player} ({_player_name}) está AFK e perdeu 1 ponto no Scoreboard Geral\n", _all_addresses)
        send_msg("terminate", _active_address)

        #tira 1 ponto do jogador AFK
        afk_player = _player_name
        try:
            create_db = open("scoreboard.txt", "x")
        except FileExistsError:
            pass
        edit_db = open("scoreboard.txt", "a")
        read_db = open("scoreboard.txt", "r")
        content = read_db.readlines()
        content_line = -1
        i = -1
        for line in content:
            i += 1
            content_data = content[i].split(" : ")
            if content_data[0] == afk_player:
                content_line = i
                final_points = int(content_data[1]) - 1
                content[i] = f"{afk_player} : {final_points}\n"
                rewrite_db = open("scoreboard.txt", "w")
                rewrite_db.writelines(content)
                rewrite_db.close()
                break
        if content_line == -1:
            edit_db.write(f"{afk_player} : -1\n")
        read_db.close()
        edit_db.close()

        print("\nWatchdog expire")

        #Mandar o jogador que não estava Afk fechar
        if _active_address == _all_addresses[0]:
            send_msg("terminate",_all_addresses[1])
        else:
            send_msg("terminate",_all_addresses[0])


        os.kill(os.getpid(), signal.SIGINT)





    def start(self):
        if self._t is None:
            self._t = threading.Timer(self.timeout, self._expire)
            self._t.start()

    def stop(self):
        if self._t is not None:
            self._t.cancel()
            self._t = None

    def refresh(self):
        if self._t is not None:
             self.stop()
             self.start()
