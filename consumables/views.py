import random

from django.http import JsonResponse
from django.shortcuts import render, redirect

from consumables.models import Consumables
from myclass.main.content import change_content
from users.models import Player, Equipping


# Create your views here.
def HP_to_full(hero: Player.objects):
    hero.now_HP = hero.HP + Equipping.HP
    hero.save()


def MP_to_full(hero: Player.objects):
    hero.now_MP = hero.MP + Equipping.MP
    hero.save()


def all_to_full(hero: Player.objects):
    hero.now_HP = hero.HP + Equipping.HP
    hero.now_MP = hero.MP + Equipping.MP
    hero.save()


def use_co(hero: Player.objects, co: Consumables.objects):
    eval(co.method + '(hero)')


def diao(hero: Player.objects) -> Consumables.objects:
    name = random.random()
    if 0.48 <= name <= 0.52:
        name = '全能药'
    elif name <= 0.1:
        name = '大红药'
    elif name >= 0.9:
        name = '大蓝药'
    else:
        return
    co = Consumables.objects.get(name=name)
    return co


def detail(request, content, res_id, name):
    if request.method == 'GET':
        admin = 'Super_Game_Admin' in request.COOKIES.keys()
        resource_type = '消耗品'
        if not res_id:
            resource_list = Consumables.objects.all()
        else:
            resource = Consumables.objects.get(id=res_id)
            resource = [
                ('name', '名称', resource.name),
                ('cover', '图标', '<img src="/media/' + resource.cover.name + '">'),
                ('menu', '介绍', resource.menu),
                ('gold', '所需金币', resource.gold),
                # ('method', '使用效果', resource.method),
            ]
        return render(request, 'game/detail.html', locals())
    elif request.method == 'POST':
        resource = Consumables.objects.get(id=res_id)
        return change_content(request, name, resource)


def append(request, content):
    if request.method == 'GET':
        resource_type = '消耗品'
        resource = [
            ('name', '名称'),
            ('cover', '图标'),
            ('menu', '介绍'),
            ('gold', '所需金币'),
            # ('method', '使用效果', resource.method),
        ]
        return render(request, 'game/append.html', locals())
    elif request.method == 'POST':
        resource = Consumables.objects.create(
            name=request.POST.get('name'),
            menu=request.POST.get('menu'),
            gold=request.POST.get('gold'),
        )
        if 'cover' in request.FILES.keys():
            resource.cover = request.FILES.get('cover')
        resource.save()
        return redirect('/detail/equipment/' + str(resource.id))
        # return render(request, 'game/append.html')


def delete(request, content, res_id):
    if request.method == 'GET':
        resource = Consumables.objects.get(id=res_id)
        resource.delete()
        if resource.cover.name != 'none.jpg':
            resource.cover.delete()
        return redirect('/detail/consumable/')
    elif request.method == 'POST':
        resource = {}
        for consumable in Consumables.objects.all():
            resource[consumable.id] = consumable.name
        return JsonResponse({'resource': resource})
