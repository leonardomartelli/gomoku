from models import *
from gomoku import Gomoku
import sys
import re


PATTERN = re.compile(r'([-ox])(\d*)')


def play(game, player, play, responder):
    result = game.play(player, play)
    return result
    #responder.respond(player, play, result)


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


def decompress(compressed):
    count = 0
    table = ''

    for match in PATTERN.findall(compressed):
        qnt_str = match[1]

        qnt = 1
        if qnt_str != '':
            qnt = int(qnt_str)

        for _ in range(qnt):
            table += match[0]
            count += 1

            if count == 15:
                table += '\n'
                count = 0
    return table


gomoku = Gomoku()

player = 'o'
c = 0

while (True):
    user_input = input().split()

    play_req = PlayRequest(int(user_input[0]), int(user_input[1]))

    if c % 2 == 0:
        player = 'x'
    else:
        player = 'o'

    c += 1

    result = play(gomoku, player, play_req, None)

    print(result)
    table_compressed = compress(gomoku.serialize())
    print(decompress(table_compressed))
    print(table_compressed)
