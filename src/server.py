from models import *
import sys

TABLE_SIZE = 14
EMPTY = '-'

table = [ [ EMPTY for i in range(TABLE_SIZE + 1) ] for j in range(TABLE_SIZE + 1) ]

def horizontal_win(player, play):
    line = table[play.line]
    streak = 0
    
    for column in range(play.column - 4, play.column + 5):
        if column < 0:
            continue
        if column > TABLE_SIZE or streak == 5:
            break

        if column == play.column or line[column] == player:
            streak += 1
        else:
            streak = 0

    return streak == 5

def vertical_win(player, play):
    streak = 0
    
    for line in range(play.line - 4, play.line + 5):
        if line < 0:
            continue
        if line > TABLE_SIZE or streak == 5:
            break

        if play.line == line or table[line][play.column] == player:
            streak += 1
        else:
            streak = 0

    return streak == 5

def left_diagonal_win(player, play):
    streak = 0
    for offset in range(-4,5):
        line = play.line - offset
        column = play.column + offset

        if line < 0 or column < 0:
            continue
        if line > TABLE_SIZE or column > TABLE_SIZE or streak == 5:
            break

        if offset == 0 or table[line][column] == player:
            streak += 1
        else:
            streak = 0

    return streak == 5

def right_diagonal_win(player, play):
    streak = 0
    for offset in range(-4,5):
        line = play.line + offset
        column = play.column + offset

        if line < 0 or column < 0:
            continue
        if line > TABLE_SIZE or column > TABLE_SIZE or streak == 5:
            break

        if offset == 0 or table[line][column] == player:
            streak += 1
        else:
            streak = 0

    return streak == 5

def diagonal_win(player, play):
    return left_diagonal_win(player, play) or right_diagonal_win(player, play)

def check(player, play):
    return vertical_win(player, play) or horizontal_win(player, play) or diagonal_win(player, play)

def play(player, play, responder):
    result = 0

    if table[play.line][play.column] != EMPTY:
        result = -1
    else:
        if check(player, play):
            result = 1

        table[play.line][play.column] = player
    
    return result
    ##responder.respond(player, play, result)

def print_table():
    for line in table:
        str_line = ''
        for column in line:
            str_line += column
        print(f'{str_line}\n')


cont = 0
while(True):
    play_input = input().split()
    player = 'o'
    
    if cont % 2 > 0:
        player = 'x'

    play_req = PlayRequest( int(play_input[0]), int(play_input[1]))

    r =play(player, play_req, None)
    print_table()
    print(r)
    cont += 1