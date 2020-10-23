import random

from django.http import JsonResponse
from django.shortcuts import render, redirect

from monsters.models import Monster
from myclass.main.content import change_content
from users.models import Player


# Create your views here.
def tower_boss(hero: Player.objects) -> dict:
    result = boss_100(hero)
    result['name'] = '你的心魔'
    result['menu'] = '你的心魔终于出现了，战胜它，证明你自己！'
    return result


def forest_boss(hero: Player.objects) -> dict:
    hero = random.choice(Player.objects.filter(sex=hero.sex, pos=hero.pos))
    result = boss_100(hero)
    result['name'] = '心魔双子'
    result['menu'] = '似乎和那个心魔有种密不可分的关系。总之，战胜它！'
    return result


def boss_100(hero: Player.objects) -> dict:
    HP = 1000 * round(hero.HP * 1.1 ** (33 - hero.lv))
    MP = 1000 * round(hero.MP * 1.1 ** (33 - hero.lv))
    att = 10 * round(hero.att * 1.15 ** (33 - hero.lv))
    baoji = hero.baoji + 0.02 * (33 - hero.lv)
    xiaoguo = hero.xiaoguo + 0.05 * (33 - hero.lv)
    shanghai = hero.shanghai + 0.05 * (33 - hero.lv)
    gailv = 1 - 1 / (hero.shanghai + 0.05 * (33 - hero.lv))
    run = 0
    exp = 10000
    gold = 10000
    return locals()


def boss_20(mon: Monster.objects, vary: int) -> dict:
    name = '被心魔侵染的' + mon.name
    menu = '它曾经是' + mon.name + '，但是它现在被心魔侵染了心智'
    HP = 10 * mon.HP * vary
    MP = 10 * mon.MP * vary
    att = round(mon.att * 0.7 * (vary + 1))
    baoji = mon.baoji * (1 + 0.1 * vary)
    xiaoguo = mon.xiaoguo * (2 - 0.1 * vary)
    shanghai = mon.shanghai * (2 - 0.1 * vary)
    gailv = mon.gailv * (1 + 0.1 * vary)
    run = 0.01
    exp = mon.exp * vary
    gold = mon.gold * vary
    return locals()


def detail(request, content, res_id, name):
    if request.method == 'GET':
        admin = 'Super_Game_Admin' in request.COOKIES.keys()
        resource_type = '怪物'
        if not res_id:
            resource_list = Monster.objects.all()
        else:
            resource = Monster.objects.get(id=res_id)
            resource = [
                ('name', '名称', resource.name),
                ('cover', '图标', '<img src="/media/' + resource.cover.name + '">'),
                ('action', '动作', '<img src="/media/' + resource.action.name + '">'),
                ('menu', '介绍', resource.menu),
                ('HP', '生命值', resource.HP),
                ('MP', '法力值', resource.MP),
                ('att', '攻击力', resource.att),
                ('baoji', '暴击概率', resource.baoji),
                ('xiaoguo', '暴击效果', resource.xiaoguo),
                ('gailv', '技能释放概率', resource.gailv),
                ('shanghai', '技能伤害加成', resource.shanghai),
                ('exp', '击杀经验值', resource.exp),
                ('gold', '掉落金币数', resource.gold),
                ('run', '逃跑概率', resource.run),
            ]
        return render(request, 'game/detail.html', locals())
    elif request.method == 'POST':
        resource = Monster.objects.get(id=res_id)
        return change_content(request, name, resource)


def append(request, content):
    if request.method == 'GET':
        resource_type = '怪物'
        resource = [
            ('name', '名称'),
            ('cover', '图标'),
            ('action', '动作'),
            ('menu', '介绍'),
            ('HP', '生命值'),
            ('MP', '法力值'),
            ('att', '攻击力'),
            ('baoji', '暴击概率'),
            ('xiaoguo', '暴击效果'),
            ('gailv', '技能释放概率'),
            ('shanghai', '技能伤害加成'),
            ('exp', '击杀经验值'),
            ('gold', '掉落金币数'),
            ('run', '逃跑概率'),
        ]
        return render(request, 'game/append.html', locals())
    elif request.method == 'POST':
        resource = Monster.objects.create(
            name=request.POST.get('name'),
            menu=request.POST.get('menu'),
            HP=request.POST.get('HP'),
            MP=request.POST.get('MP'),
            att=request.POST.get('att'),
            baoji=request.POST.get('baoji'),
            xiaoguo=request.POST.get('xiaoguo'),
            gailv=request.POST.get('gailv'),
            shanghai=request.POST.get('shanghai'),
            gold=request.POST.get('gold'),
            exp=request.POST.get('exp'),
            run=request.POST.get('run'),
        )
        if 'cover' in request.FILES.keys():
            resource.cover = request.FILES.get('cover')
        if 'action' in request.FILES.keys():
            resource.action = request.FILES.get('action')
        resource.save()
        return redirect('/detail/monster/' + str(resource.id))
        # return render(request, 'game/append.html')


def delete(request, content, res_id):
    if request.method == 'GET':
        resource = Monster.objects.get(id=res_id)
        resource.delete()
        if resource.cover.name != 'none.png':
            resource.cover.delete()
        if resource.action.name != 'none.png':
            resource.action.delete()
        return redirect('/detail/monster/')
    elif request.method == 'POST':
        resource = {}
        for monster in Monster.objects.all():
            resource[monster.id] = monster.name
        return JsonResponse({'resource': resource})
