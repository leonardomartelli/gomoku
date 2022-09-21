class PlayRequest:
    def __init__(self, line, column):
        self.line = line
        self.column = column
    
    def serialize(self):
        return f'{self.line};{self.column}'

class Requester:
    def __init__(self, socket):
        self.socket = socket
    
    def request(self, req):
        self.socket.send(req.serialize())