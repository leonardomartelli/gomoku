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


class PlayResponse:
    def __init__(self, result, table):
        self.result = result
        self.table = table

    @classmethod
    def new(cls, data):
        return cls.deserialize(data)

    def serialize(self):
        return f'play:{self.result};{self.table}'

    @classmethod
    def deserialize(cls, data):
        splitted = data.split(';')
        return cls(splitted[0].split(':')[1], splitted[1])


class ErrorResponse:
    def __init__(self, message, table):
        self.message = message
        self.table = table

    @classmethod
    def new(cls, data):
        return cls.deserialize(data)

    def serialize(self):
        return f'error:{self.message};{self.table}'

    @classmethod
    def deserialize(cls, data):
        splitted = data.split(';')
        return cls(splitted[0].split(':')[1], splitted[1])


class ResultResponse:
    def __init__(self, result, table):
        self.result = result
        self.table = table

    @classmethod
    def new(cls, data):
        return cls.deserialize(data)

    def serialize(self):
        return f'result:{self.result};{self.table}'

    @classmethod
    def deserialize(cls, data):
        splitted = data.split(';')
        return cls(splitted[0].split(':')[1], splitted[1])


class Requester:
    def __init__(self, socket):
        self.socket = socket

    def request(self, req):
        self.request_str(req.serialize())

    def request_str(self, message):
        print(message)
        self.socket.send(message.encode())

    def receive(self):
        return self.socket.recv(1024).decode()

    def close(self):
        self.socket.close()
