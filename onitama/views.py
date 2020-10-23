import html
import json
import re

from django.views import View
from dwebsocket import accept_websocket

from django.shortcuts import render

from onitama.connect import Server
from users.models import User
from users.views import check_token


# Create your views here.
def index(request):
    content = 'hall'
    return render(request, 'onitama/index.html', locals())


server = Server()


@accept_websocket
def connect(request):
    if not request.is_websocket():
        return render(request, 'game/index.html', locals())

    for message in request.websocket:
        user_id = check_token(request)
        if not user_id:
            request.websocket.send(json.dumps({"code": '0'}).encode())
        elif not message:
            print('收到了一条空信息！')
        elif request.websocket.is_closed():
            # request.websocket.send(json.dumps({"code": '400'}).encode())
            del server.client[user_id]
        elif message[:2] != '#!' or message[-2:] != '!#':
            request.websocket.send(json.dumps({'error': '别想乱搞！'}).encode())
        else:
            server.client[user_id] = request.websocket
            message = message.decode()[2: -2]
            user = User.objects.get(user_id=user_id)

            # 可能会报错，报错返回错误原因
            message, client_list = server.get_message(message, user, request.websocket)

            for _ in client_list:
                server.client[_].send(json.dumps({"result": message}).encode())
