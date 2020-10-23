import random

from django.http import JsonResponse
from django.shortcuts import render, redirect

from heroes.models import Hero, Info
from myclass.main.content import change_content
from users.models import Player, Equipping


# Create your views here.
def lv_need_exp(lv: int) -> int:
    exp_lv = 0
    exp = 0
    while exp_lv <= lv:
        exp += lv
        exp_lv += 1
    return 10 * exp


def lv_up(hero: Player.objects) -> (int, int):
    up = 0
    equ = Equipping.objects.get(hero=hero)
    while hero.exp >= lv_need_exp(hero.lv):
        hero.exp -= lv_need_exp(hero.lv)
        hero.lv += 1

        hero.HP = round(hero.HP * 1.1)
        hero.now_HP = hero.HP + equ.HP
        hero.MP = round(hero.MP * 1.1)
        hero.now_MP = hero.MP + equ.MP
        hero.att = round(hero.att * random.uniform(1.05, 1.25))
        hero.baoji = hero.baoji + 0.003
        hero.xiaoguo = hero.xiaoguo + 0.05
        hero.shanghai = hero.shanghai + 0.05

        hero.save()
        up += 1
    return up, lv_need_exp(hero.lv) - hero.exp


def new_hero(hero_info):
    pos = hero_info['pos']
    HP = hero_info['HP']
    MP = hero_info['MP']
    att = hero_info['att']
    baoji = hero_info['baoji']
    xiaoguo = hero_info['xiaoguo']
    shanghai = hero_info['shanghai']
    menu = hero_info['menu']
    return [
        Info.objects.create(
            hero=Hero.objects.create(pos=pos, sex='男', menu=menu),
            max_HP=1.1 * (HP + 25), min_HP=1.1 * (HP - 25),
            max_MP=0.8 * (MP + 10), min_MP=0.8 * (MP - 10),
            max_att=1.1 * (att + 5), min_att=1.1 * (att - 5),
            max_baoji=(baoji + 0.02) + 0.05, min_baoji=(baoji - 0.02) + 0.05,
            max_xiaoguo=(xiaoguo + 0.1), min_xiaoguo=(xiaoguo - 0.1),
            max_shanghai=(shanghai + 0.1), min_shanghai=(shanghai - 0.1),
        ),
        Info.objects.create(
            hero=Hero.objects.create(pos=pos, sex='女', menu=menu),
            max_HP=0.9 * (HP + 25), min_HP=0.9 * (HP - 25),
            max_MP=1.2 * (MP + 10), min_MP=1.2 * (MP - 10),
            max_att=0.9 * (att + 5), min_att=0.9 * (att - 5),
            max_baoji=(baoji + 0.02), min_baoji=(baoji - 0.02),
            max_xiaoguo=(xiaoguo + 0.1) + 0.1, min_xiaoguo=(xiaoguo - 0.1) + 0.1,
            max_shanghai=(shanghai + 0.1) + 0.1, min_shanghai=(shanghai - 0.1) + 0.1,
        ),
    ]


def detail(request, content, res_id, name):
    if request.method == 'GET':
        admin = 'Super_Game_Admin' in request.COOKIES.keys()
        resource_type = '英雄'
        if not res_id:
            resource_list = Hero.objects.all()
        else:
            resource = Hero.objects.get(id=res_id)
            resource = [
                ('pos', '职业', resource.sex + resource.pos),
                ('menu', '介绍', resource.menu),
                ('cover', '图标', '<img src="/media/' + resource.cover.name + '">'),
                ('action', '动作', '<img src="/media/' + resource.action.name + '">'),
                ('HP', '初始生命值', str(resource.info.min_HP) + '~' + str(resource.info.max_HP)),
                ('MP', '初始法力值', str(resource.info.min_MP) + '~' + str(resource.info.max_MP)),
                ('att', '初始攻击力', str(resource.info.min_att) + '~' + str(resource.info.max_att)),
                ('baoji', '初始暴击概率', str(resource.info.min_baoji) + '~' + str(resource.info.max_baoji)),
                ('xiaoguo', '初始暴击效果', str(resource.info.min_xiaoguo) + '~' + str(resource.info.max_xiaoguo)),
                ('shanghai', '初始技能伤害', str(resource.info.min_shanghai) + '~' + str(resource.info.max_shanghai)),
            ]
        return render(request, 'game/detail.html', locals())
    elif request.method == 'POST':
        resource = Hero.objects.get(id=res_id)
        return change_content(request, name, resource)


def append(request, content):
    if request.method == 'GET':
        resource_type = '英雄'
        resource = [
            ('pos', '职业'),
            ('menu', '介绍'),
            ('cover', '图标'),
            ('action', '动作'),
            ('HP', '初始生命值'),
            ('MP', '初始法力值'),
            ('att', '初始攻击力'),
            ('baoji', '初始暴击概率'),
            ('xiaoguo', '初始暴击效果'),
            ('shanghai', '初始技能伤害'),
        ]
        return render(request, 'game/append.html', locals())
    elif request.method == 'POST':
        hero_info = {
            'pos': request.POST.get('pos'),
            'menu': request.POST.get('menu'),
            'HP': int(request.POST.get('HP')),
            'MP': int(request.POST.get('MP')),
            'att': int(request.POST.get('att')),
            'baoji': float(request.POST.get('baoji')),
            'xiaoguo': float(request.POST.get('xiaoguo')),
            'shanghai': float(request.POST.get('shanghai')),
        }
        resources = new_hero(hero_info)
        for resource in resources:
            if 'cover' in request.FILES.keys():
                resource.hero.cover = request.FILES.get('cover')
            if 'action' in request.FILES.keys():
                resource.hero.action = request.FILES.get('action')
            resource.save()
        return redirect('/detail/hero/')
        # return render(request, 'game/append.html')


def delete(request, content, res_id):
    if request.method == 'GET':
        pos = Hero.objects.get(id=res_id).pos
        resources = Hero.objects.filter(pos=pos)
        for resource in resources:
            if resource.cover.name != 'none.png':
                resource.cover.delete()
            if resource.action.name != 'none.png':
                resource.action.delete()
            resource.delete()
        return redirect('/detail/hero/')
    elif request.method == 'POST':
        resource = {}
        for hero in Hero.objects.all():
            resource[hero.id] = hero.name
        return JsonResponse({'resource': resource})
