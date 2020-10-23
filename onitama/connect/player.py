"""
    玩家
"""


class Player(object):
    def __init__(self, color, user):
        self.color = color
        self.user = user
        self.pieces = []
        self.cards = []
