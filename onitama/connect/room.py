"""
    房间，
    初始化的配置
    交互过程
"""
from onitama.connect.card import Card
from onitama.connect.piece import Piece
from onitama.connect.player import Player


class Room(object):
    def __init__(self, r, b):
        """
        玩家客户端->玩家对象
        """
        self.id = b, r

        card_list = Card.div_card()
        self.victory = ''

        self.tiv = Player('', 0)
        self.tiv.cards = card_list[:3]
        self.siv = Player('', 0)
        self.siv.cards = card_list[3:]

        if card_list[2].seq == 'red':
            pr, pb = self.tiv, self.siv
        elif card_list[2].seq == 'blue':
            pb, pr = self.tiv, self.siv
        else:
            raise

        pr.color, pr.user = 'red', r
        pr.pieces = [Piece((_, 5), not _-3) for _ in range(1, 6)]
        pb.color, pb.user = 'blue', b
        pb.pieces = [Piece((_, 1), not _-3) for _ in range(1, 6)]

    def choose(self, position: tuple):
        for piece in self.tiv.pieces:
            if piece.position == position:
                return piece

    def move(self, piece: Piece, position: tuple):
        piece.position = position
        vic = {'red': (3, 1), 'blue': (3, 5)}
        if piece.boss and piece.position == vic[self.tiv.color]:
            self.victory = self.tiv.color
        return self.eat(position)

    def eat(self, position: tuple):
        for piece in self.siv.pieces:
            if piece.position == position:
                self.siv.pieces.remove(piece)
                if piece.boss:
                    self.victory = self.tiv.color
                break
        return position

    def rel_conn(self, card_name: str):
        for card in self.tiv.cards:
            if card.name == card_name:
                self.tiv.cards.remove(card)
                self.siv.cards.append(card)
                self.tiv, self.siv = self.siv, self.tiv
                break

    def name(self):
        r_cards, b_cards = [], []
        if self.tiv.cards[2].seq == 'red':
            r, b = self.tiv, self.siv
        elif self.tiv.cards[2].seq == 'blue':
            b, r = self.tiv, self.siv
        else:
            raise
        for card in r.cards:
            r_cards.append(card.name)
        for card in b.cards:
            b_cards.append(card.name)
        return (r.user, r_cards), (b.user, b_cards)
