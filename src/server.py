from models import *
from gomoku import Gomoku
import sys
import re
import socket


def play(game, play):
    result = game.play(play)
    return result

# returns a string with the the pattern {character}{character
# repetitions} (if 'character repetitions' == 1, only 'character'
# is present)
# example: x-35ox-11x-o-10x2o3x-9x-o-o-11o-2o-10x-116x


def compress(table):
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


def receive(play_req, player):
    result = play(gomoku, player, play_req, None)
    print(result)

    return compress(gomoku.serialize())


def initialize_socket(ip, port):
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.bind((ip, port))
    _socket.listen(255)

    return _socket


def route_request(data):
    return PlayRequest.new(data)


def register(request, socket, client):
    if len(clients) == 2:
        return None

    clients[request.id] = (socket, client)

    if len(clients) == 1:
        return 'x'
    else:
        return 'o'


def initialize_players(socket, clients):
    s1, client = socket.accept()

    req_1 = Requester(s1)

    clients.append((req_1, client, 'x'))

    print(f'client {client} initiated - x')

    s2, client = socket.accept()

    req_2 = Requester(s2)

    clients.append((req_2, client, 'o'))

    print(f'client {client} initiated - o')

    req_1.request_str('x')
    req_2.request_str('o')


def end_game(clients, winner, game):
    for (connection, client, player) in clients:
        connection.request(ResultResponse(winner == player, game))
        connection.close()


def send_state(clients, table_compressed):
    for (connection, client, player) in clients:
        print(f' sent to {client} - player {player}')
        connection.request(PlayResponse(result, table_compressed))


if len(sys.argv) != 2:
    print(f'{sys.argv[0]} <port>')
    sys.exit(0)

ip = 'localhost'

port = int(sys.argv[1])

clients = []

socket = initialize_socket(ip, port)

initialize_players(socket, clients)

gomoku = Gomoku()

cont = 0

while True:

    (connection, client, player) = clients[cont % 2]

    data = connection.receive()

    request = route_request(data)

    result = play(gomoku, request)

    table_compressed = compress(gomoku.serialize())
    if result == -1:
        connection.request(ErrorResponse('ALREADY_PLAYED', table_compressed))
    elif result == 1:
        end_game(clients, request.player, table_compressed)
        break
    else:
        send_state(clients, table_compressed)
        cont += 1
