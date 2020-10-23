"""
    棋子
"""


class Piece(object):
    def __init__(self, position: tuple, boss: bool = False):
        self.position = position
        self.boss = boss

    def move(self, method: tuple):
        self.position = (self.position[0] + method[0],
                         self.position[1] + method[1])
        return self.position


if __name__ == '__main__':
    p = Piece((3, 5))
