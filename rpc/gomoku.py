TABLE_SIZE = 14
EMPTY = '-'


class Gomoku:
    def __init__(self):
        self.table = [[EMPTY for i in range(TABLE_SIZE + 1)]
                      for j in range(TABLE_SIZE + 1)]

    def serialize(self):
        s = ''
        for line in self.table:
            for entry in line:
                s += entry
        return s

    def horizontal_win(self, player, play):

        play_line = int(play.line)
        play_column = int(play.column)
        line = self.table[play_line]
        streak = 0

        for column in range(play_column - 4, play_column + 5):
            if column < 0:
                continue
            if column > TABLE_SIZE or streak == 5:
                break

            if column == play_column or line[column] == player:
                streak += 1
            else:
                streak = 0

        return streak == 5

    def vertical_win(self, player, play):
        streak = 0

        play_line = int(play.line)
        play_column = int(play.column)
        for line in range(play_line - 4, play_line + 5):
            if line < 0:
                continue
            if line > TABLE_SIZE or streak == 5:
                break

            if play.line == line or self.table[line][play_column] == player:
                streak += 1
            else:
                streak = 0

        return streak == 5

    def left_diagonal_win(self, player, play):
        streak = 0
        for offset in range(-4, 5):
            line = int(play.line) - offset
            column = int(play.column) + offset

            if line < 0 or column < 0:
                continue
            if line > TABLE_SIZE or column > TABLE_SIZE or streak == 5:
                break

            if offset == 0 or self.table[line][column] == player:
                streak += 1
            else:
                streak = 0

        return streak == 5

    def right_diagonal_win(self, player, play):
        streak = 0
        for offset in range(-4, 5):
            line = int(play.line) + offset
            column = int(play.column) + offset

            if line < 0 or column < 0:
                continue
            if line > TABLE_SIZE or column > TABLE_SIZE or streak == 5:
                break

            if offset == 0 or self.table[line][column] == player:
                streak += 1
            else:
                streak = 0

        return streak == 5

    def diagonal_win(self, player, play):
        return self.left_diagonal_win(player, play) \
            or self.right_diagonal_win(player, play)

    def check(self, player, play):
        return self.vertical_win(player, play) \
            or self.horizontal_win(player, play) \
            or self.diagonal_win(player, play)

    def play(self, play):
        result = 0

        line = int(play.line)
        column = int(play.column)

        if not self.validate_play(line, column):
            result = -1
        else:
            if self.check(play.player, play):
                result = 1

            self.table[line][column] = play.player

        return result

    def validate_play(self, line, column):
        outside_table = line < 0 or line > 14 or column < 0 or column > 14
        is_occupied = self.table[line][column] != EMPTY
        return not outside_table and not is_occupied
