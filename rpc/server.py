import xmlrpc.server
import sys

from gomoku import Gomoku
from models import *
from enum import Enum


class GomokuStatus(Enum):
    WAITING_PLAYERS = 1
    GAME_STARTED = 2
    GAME_FINISHED = 3


class GomokuGame:
    def __init__(self):
        self.gomoku = Gomoku()
        self.game_status = GomokuStatus.WAITING_PLAYERS
        self.players = []
        self.cont = 0

    def start_game(self):
        if len(self.players) == 2:
            print(f'game has started')
            self.gomoku = Gomoku()
            self.game_status = GomokuStatus.GAME_STARTED

    def get_table(self):
        return self.compress()

    def get_game_status(self):
        return self.game_status.value

    def get_current_player(self):
        return self.players[self.cont % 2][1]

    def add_player(self, new_player):
        if len(self.players) == 2:
            return None

        if len(self.players) == 1:
            self.players.append((new_player, 'x'))
            print(f'client {new_player} joined - x')
            self.start_game()
            return 'x'
        else:
            self.players.append((new_player, 'o'))
            print(f'client {new_player} joined - o')
            return 'o'

    def play(self, line, column, player):
        if (self.game_status == GomokuStatus.WAITING_PLAYERS):
            return False, 'Esperando por jogadores'
        elif (self.game_status == GomokuStatus.GAME_FINISHED):
            return False, 'O jogo já acabou'

        if player != self.get_current_player():
            return False, 'Não é seu turno'
        else:
            play_request = PlayRequest(line, column, player)
            result = self.gomoku.play(play_request)

            if result == -1:
                return False, 'Jogada inválida'
            elif result == 1:
                self.end_game(player)
                return True, ''
            else:
                self.cont += 1
                return True, ''

    def end_game(self, player):
        self.game_status = GomokuStatus.GAME_FINISHED
        self.winner = player
        self.players = []

    def get_winner(self):
        if (self.game_status == GomokuStatus.GAME_FINISHED):
            return self.winner

    # returns a string with the the pattern {character}{character
    # repetitions} (if 'character repetitions' == 1, only 'character'
    # is present)
    # example: x-35ox-11x-o-10x2o3x-9x-o-o-11o-2o-10x-116x

    def compress(self):
        table = self.gomoku.serialize()
        compressed = ''

        current = table[0]
        count = 1

        for entry in table[1:]:
            if entry == current:
                count += 1
            else:
                compressed += current

                if count != 1:
                    compressed += str(count)

                current = entry
                count = 1

        compressed += current
        if count != 1:
            compressed += str(count)

        return compressed


if len(sys.argv) != 2:
    print(f'{sys.argv[0]} <port>')
    sys.exit(0)

ip = 'localhost'

port = int(sys.argv[1])

server = xmlrpc.server.SimpleXMLRPCServer(("localhost", port))

gomoku = GomokuGame()

server.register_function(gomoku.get_game_status, "get_game_status")
server.register_function(gomoku.add_player, "add_player")
server.register_function(gomoku.get_current_player, "get_current_player")
server.register_function(gomoku.get_winner, "get_winner")
server.register_function(gomoku.get_table, "get_table")
server.register_function(gomoku.play, "play")

server.serve_forever()
