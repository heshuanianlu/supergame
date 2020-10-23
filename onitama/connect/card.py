"""
    牌
"""
import random


class Card(object):
    def __init__(self, name: str, method: list, seq: str):
        self.name = name
        self.method = method
        self.seq = seq
        self.img = ''

    def position(self, position: tuple):
        result = []
        for method in self.method:
            result.append((method[0] + position[0],
                           method[1] + position[1]))
        return result

    @staticmethod
    def div_card():
        return random.sample(LI, 5)


LI = [
    Card('猿', [(-1, 1), (1, 1), (-1, -1), (1, -1)], 'blue'),
    Card('象', [(1, 0), (-1, 0), (1, 1), (-1, 1)], 'red'),
    Card('蟹', [(0, 1), (2, 0), (-2, 0)], 'blue'),
    Card('猪', [(0, 1), (1, 0), (-1, 0)], 'red'),
    Card('虎', [(0, 2), (0, -1)], 'blue'),
    Card('龙', [(-2, 1), (2, 1), (-1, -1), (1, -1)], 'red'),
    Card('鹅', [(1, 0), (-1, 1), (-1, 0), (1, -1)], 'blue'),
    Card('鸡', [(1, 0), (1, 1), (-1, 0), (-1, -1)], 'red'),
    Card('兔', [(2, 0), (1, 1), (-1, -1)], 'blue'),
    Card('蛙', [(-2, 0), (-1, 1), (1, -1)], 'red'),
    Card('鳗', [(1, 0), (-1, 1), (-1, -1)], 'blue'),
    Card('蛇', [(-1, 0), (1, 1), (1, -1)], 'red'),
    Card('牛', [(0, 1), (0, -1), (1, 0)], 'blue'),
    Card('马', [(0, 1), (0, -1), (-1, 0)], 'red'),
    Card('鹤', [(0, 1), (1, -1), (-1, -1)], 'blue'),
    Card('螳螂', [(0, -1), (1, 1), (-1, 1)], 'red'),
]
