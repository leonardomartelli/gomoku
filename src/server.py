from models import *
from gomoku import Gomoku
import sys

def play(game, player, play, responder):
    result = game.play(player, play)
    responder.respond(player, play, result)

gomuku = Gomoku()