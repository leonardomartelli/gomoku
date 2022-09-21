from models import *
import sys

def connect(ip, port):
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((ip, port))
    return Requester(socket)

def play(requester, line, column):
    requester.play(PlayRequest(line, column))

