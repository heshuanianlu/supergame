"""
将数据存于数据库中
"""

import os

from heroes.views import new_hero
from supergame.settings import BASE_DIR
from consumables.models import Consumables
from equipments.models import Equipment
from monsters.models import Monster
from myclass.ready.hero import zs, fs, ck, gj
from myclass.ready.map import ma


def ys():
    sa = BASE_DIR + r'/myclass/ready/'
    more = os.listdir(sa + 'equipment')
    for i in more:
        try:
            with open(sa + '/equipment/' + i, 'r', encoding='gbk') as f:
                al = f.read().split('\n')
                print(Equipment.objects.create(
                    name=i[:-4],
                    menu=al[0],
                    type=al[1],
                    HP=int(al[2]),
                    MP=int(al[3]),
                    att=int(al[4]),
                    baoji=float(al[5]),
                    xiaoguo=float(al[6]),
                    shanghai=float(al[7]),
                    gold=int(al[8]),
                ))
        except Exception as e:
            print('ready ys_equipment error', e)

    more = os.listdir(sa + 'monster')
    for i in more:
        try:
            with open(sa + '/monster/' + i, 'r', encoding='gbk') as f:
                al = f.read().split('\n')
                print(Monster.objects.create(
                    name=i[:-4],
                    menu=al[0],
                    HP=int(al[1]),
                    MP=int(al[2]),
                    att=int(al[3]),
                    baoji=float(al[4]),
                    xiaoguo=float(al[5]),
                    shanghai=float(al[6]),
                    gailv=float(al[7]),
                    run=float(al[8]),
                    exp=int(al[9]),
                    gold=int(al[10]),
                ))
        except Exception as e:
            print('ready ys_monster error', e)


def th():
    Consumables.objects.create(
        name='大红药', gold=30,
        menu='可以把生命值恢复至满',
        method='HP_to_full',
    )
    Consumables.objects.create(
        name='大蓝药', gold=30,
        menu='可以把法力值恢复至满',
        method='MP_to_full',
    )
    Consumables.objects.create(
        name='全能药', gold=50,
        menu='可以把生命值和法力值恢复至满',
        method='all_to_full',
    )


def he():
    for h in [zs, fs, ck, gj]:
        new_hero(h)
    ma()
