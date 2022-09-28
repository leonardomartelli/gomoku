from models import *
import sys
import re
import socket

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


def connect(ip, port):
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.connect((ip, port))
    return Requester(_socket)


def play(requester, line, column, player):
    requester.request(PlayRequest(line, column, player))
    return requester.receive()


def route_response(data):
    if data.startswith('error:'):
        return ErrorResponse.new(data)
    elif data.startswith('result:'):
        return ResultResponse.new(data)

    return PlayResponse.new(data)


def int_try_parse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


if len(sys.argv) != 2:
    print(f'{sys.argv[0]} <port>')
    sys.exit(0)

ip = 'localhost'

port = int(sys.argv[1])

requester = connect(ip, port)

requester.request_str('')

player = requester.receive()

cont = 0

if (player == 'o'):
    cont = 1

while True:
    print(cont)
    if cont % 2 == 0:
        inputed_play = input("Digite sua jogada 'L C': ").split()

        line_number, line_success = int_try_parse(inputed_play[0])
        column_number, column_success = int_try_parse(inputed_play[1])

        if not line_success or not column_success:
            print("Jogada inválida!")
            continue

        response = play(requester,
                        line_number - 1, column_number-1, player)

    else:
        response = requester.receive()
        print('recebeu', response)

    print(response)

    result = route_response(response)

    print(format_table(result.table))

    if isinstance(result, ResultResponse):
        if result.result == 'True':
            print("Parabéns, você venceu!")
        else:
            print("Você perdeu!")
        break
    elif isinstance(result, ErrorResponse):
        print("Jogada inválida!")
    else:
        cont += 1

requester.close()
