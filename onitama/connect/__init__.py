from onitama.connect.room import Room
from users.models import User


def _print(fn):
    print(fn.__name__)
    return fn


class Server(object):
    def __init__(self):
        self.client = {}
        self.hall = []
        self.room = {}
        self.ready = []

    def get_message(self, message: str, self_id):
        message = message.split('=')
        if message[0] == 'connect':  # connect=my_id
            message, client_list = self.connect(self_id)
        elif message[0] == 'choose':  # choose=0
            user_id = int(message[1])
            message, client_list = self.choose(self_id, user_id)
        elif message[0] == 'agree=':  # agree=0
            user_id = int(message[1])
            message, client_list = self.agree(self_id, user_id)
        elif message[0] == 'refuse':  # refuse=0
            user_id = int(message[1])
            message, client_list = self.refuse(self_id, user_id)
        elif message[0] == 'action':  # action=0*8&14&15&牌
            room_id, piece, position, card_name = message[1].split('&')
            message, client_list = self.action(self_id, room_id, piece, position, card_name)
        elif message[0] == 'quit':  # quit=my_id
            message, client_list = self.close(self_id)
        else:
            message, client_list = {'command': 'error', 'error': '无效消息'}, [self.client[self_id]]
        return message, client_list

    @_print
    def connect(self, self_id):
        """检查用户当前状态，为重连返回战局，否则则返回大厅"""
        if self_id not in self.client.keys():
            message = self.change(self_id)
            client = self.hall
        else:
            message = {'command': 'error', 'error': '用户已登录'}
            client = self.client[self_id]
        return message, client

    def choose(self, self_id, user_id):
        """选择对手，给其发送对战请求。允许随机匹配。需要给自己显示等待，最多允许等待30秒"""
        client_user = self.client[user_id]
        client_self = self.client[self_id]
        if client_user in self.hall and client_self in self.hall:
            self.hall.remove(client_user)
            self.hall.remove(client_self)
            client = self_id, user_id
            self.ready.append(client)
            message = {'command': 'choose', 'tiv': self_id, 'siv': user_id}
            return message, (client_self, client_user)
        else:
            message = {'command': 'error', 'error': '你或对方不在大厅中'}
            return message, [client_self]

    def agree(self, self_id, user_id):
        """同意请求，开始对战，为两人创建房间，返回地图内容，先手情况"""
        if (user_id, self_id) in self.ready:
            room = Room(self_id, user_id)
            self.room[room.id] = room
            message = {'command': 'agree'}
            if room.tiv.cards[2].seq == 'red':
                message['red'] = room.tiv.cards
                message['blue'] = room.siv.cards
            elif room.tiv.cards[2].seq == 'blue':
                message['red'] = room.siv.cards
                message['blue'] = room.tiv.cards
            else:
                del self.room[room.id]
                return self.agree(self_id, user_id)
            return message, [self.client[user_id], self.client[self_id]]
        else:
            message = {'command': 'error', 'error': '查询不到匹配信息'}
            return message, [self.client[self_id]]

    def refuse(self, self_id, user_id):
        """拒绝请求，双方都返回大厅，为其返回大厅，为邀请者返回对方拒绝"""
        if (user_id, self_id) in self.ready:
            message = {'command': 'refuse'}
            self.ready.remove((user_id, self_id))
            self.hall.append(self.client[self_id])
            self.hall.append(self.client[user_id])
            return message, [self.client[user_id], self.client[self_id]]
        else:
            message = {'command': 'error', 'error': '查询不到匹配信息'}
            return message, [self.client[self_id]]

    def action(self, self_id, room_id, piece, position, card_name):
        """移动到某个区域，需要参数房间号，点击的人，点击的位置，移动到的位置
            如果胜利，返回胜利/失败界面，并且创建返回大厅按钮"""
        room = self.room[room_id]
        if self_id == room.tiv.user:
            piece = piece[0], piece[1]
            position = position[0], position[1]
            piece = room.choose(piece)
            room.move(piece, position)
            client = self.client[room.tiv.user], self.client[room.siv.user]
            message = {'command': 'action',
                       'piece': piece,
                       'position': position,
                       'card': card_name}
            if not room.victory:
                room.rel_conn(card_name)
            else:
                message['victory'] = room.victory
        else:
            message = {'command': 'error', 'error': '回合判定出错'}
            client = self.client[self_id]
        return message, client

    def close(self, self_id):
        """退出，删除其信息，关闭其网页"""
        del self.client[self_id]
        message = self.change(self_id)
        return message, self.hall

    def change(self, self_id):
        message = {'command': 'change', 'user_id': [], 'user_portrait': [], 'user_name': []}
        for user_id in self.hall:
            if user_id != self_id:
                user = User.objects.get(id=user_id)
                message['user_id'].append(user.id)
                message['user_cover'].append(user.portrait.name)
                message['user_name'].append(user.name)
        return message
