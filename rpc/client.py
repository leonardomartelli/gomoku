import xmlrpc.client
import sys
import re

from enum import Enum


class GomokuStatus(Enum):
    WAITING_PLAYERS = 1
    GAME_STARTED = 2
    GAME_FINISHED = 3


PATTERN = re.compile(r'([-ox])(\d*)')

# receives the compressed table that comes from
# the server and returns a formated table


def format_table(compressed):
    count = 0
    table = ''

    for match in PATTERN.findall(compressed):
        qnt_str = match[1]

        qnt = 1
        if qnt_str != '':
            qnt = int(qnt_str)

        for _ in range(qnt):
            table += ' '
            table += match[0]
            table += ' '
            count += 1

            if count % 15 == 0:
                table += f' {count // 15}\n'

    table += ' 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15'

    return table


def int_try_parse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


if len(sys.argv) != 2:
    print(f'{sys.argv[0]} <port>')
    sys.exit(0)

ip = 'localhost'

port = sys.argv[1]

server = xmlrpc.client.ServerProxy('http://' + ip + ':' + port)

player_name = ''
player = ''
last_player = ''

game_status_index = server.get_game_status()
last_status = GomokuStatus(game_status_index)
while True:
    game_status_index = server.get_game_status()
    game_status = GomokuStatus(game_status_index)

    # while the game his waiting for players
    if game_status == GomokuStatus.WAITING_PLAYERS:
        if player == '':
            player_name = input("Informe nome do jogador: ")
            player = server.add_player(player_name)
        else:
            print("Esperando por mais jogadores...")

    # when the game has finished
    elif game_status == GomokuStatus.GAME_FINISHED:
        winner = server.get_winner()
        if player == winner:
            print("Você ganhou!")
        else:
            print("Você perdeu!")
        break

    # while the game is still running
    else:
        current_player = server.get_current_player()

        # when the player turn changes, update the table
        if current_player != last_player:
            table = server.get_table()
            print(format_table(table))
            if player == current_player:
                print("Seu turno")
            else:
                print("Esperando oponente")

        # when it is this player's turn
        if current_player == player:
            inputed_play = input("Digite sua jogada 'L C': ").split()

            line_number, line_success = int_try_parse(inputed_play[0])
            column_number, column_success = int_try_parse(inputed_play[1])

            if not line_success or not column_success:
                print("Jogada inválida!")
                continue

            success, response = server.play(
                line_number - 1, column_number-1, player)  # type: ignore
            if not success:
                print(response)

        last_player = current_player
    last_status = game_status
