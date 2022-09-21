TABLE_SIZE = 14
EMPTY = '-'

class Gomoku:
    def __init__(self):
        self.table = [ [ EMPTY for i in range(self.TABLE_SIZE + 1) ] for j in range(self.TABLE_SIZE + 1) ]

    def horizontal_win(self, player, play):
        line = self.table[play.line]
        streak = 0

        for column in range(play.column - 4, play.column + 5):
            if column < 0:
                continue
            if column > self.TABLE_SIZE or streak == 5:
                break

            if column == play.column or line[column] == player:
                streak += 1
            else:
                streak = 0

        return streak == 5

    def vertical_win(self,player, play):
        streak = 0

        for line in range(play.line - 4, play.line + 5):
            if line < 0:
                continue
            if line > self.TABLE_SIZE or streak == 5:
                break

            if play.line == line or self.table[line][play.column] == player:
                streak += 1
            else:
                streak = 0

        return streak == 5

    def left_diagonal_win(self,player, play):
        streak = 0
        for offset in range(-4,5):
            line = play.line - offset
            column = play.column + offset

            if line < 0 or column < 0:
                continue
            if line > self.TABLE_SIZE or column > self.TABLE_SIZE or streak == 5:
                break

            if offset == 0 or self.table[line][column] == player:
                streak += 1
            else:
                streak = 0

        return streak == 5

    def right_diagonal_win(self, player, play):
        streak = 0
        for offset in range(-4,5):
            line = play.line + offset
            column = play.column + offset

            if line < 0 or column < 0:
                continue
            if line > self.TABLE_SIZE or column > self.TABLE_SIZE or streak == 5:
                break

            if offset == 0 or self.table[line][column] == player:
                streak += 1
            else:
                streak = 0

        return streak == 5

    def diagonal_win(self,player, play):
        return self.left_diagonal_win(player, play) \
            or self.right_diagonal_win(player, play)

    def check(self,player, play):
        return self.vertical_win(player, play) \
            or self.horizontal_win(player, play) \
            or self.diagonal_win(player, play)

    def play(self, player, play):
        result = 0

        if self.table[play.line][play.column] != EMPTY:
            result = -1
        else:
            if self.check(player, play):
                result = 1

            self.table[play.line][play.column] = player

        return result