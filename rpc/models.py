
class PlayRequest:
    def __init__(self, line, column, player):
        self.line = line
        self.column = column
        self.player = player

    @classmethod
    def new(cls, data):
        return cls.deserialize(data)

    def serialize(self):
        return f'play:{self.line};{self.column};{self.player}'

    @classmethod
    def deserialize(cls, data):
        splitted = data.split(';')

        return cls(splitted[0].split(':')[1], splitted[1], splitted[2])
