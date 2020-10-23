from django.http import JsonResponse
from django.shortcuts import render, redirect

from equipments.models import Equipment
from myclass.main.content import change_content
from users.models import Player, Equipping, Bag, Store

# Create your views here.
t_type = {
    '头部': 'head',
    '面部': 'face',
    '身体': 'body',
    '背部': 'back',
    '腰部': 'waist',
    '臂部': 'arm',
    '腿部': 'leg',
    '左手': 'l_hand',
    '右手': 'r_hand',
    '足具': 'feet',
}


def change_hao(equipment_action):
    def bai(hero: Player.objects, equipment: Equipment.objects):
        equipping = Equipping.objects.get(hero=hero)
        bai_HP = hero.now_HP / (equipping.HP + hero.HP)
        bai_MP = hero.now_MP / (equipping.MP + hero.MP)
        equipment_action(hero, equipment)  # 改变了equipping，需要重新获取
        equipping = Equipping.objects.get(hero=hero)
        hero.now_HP = (equipping.HP + hero.HP) * bai_HP
        hero.now_MP = (equipping.MP + hero.MP) * bai_MP
        hero.save()

    return bai


@change_hao
def equipe(hero: Player.objects, equipment: Equipment.objects):
    bag = Bag.objects.get(hero=hero)
    equipping = Equipping.objects.get(hero=hero)
    try:
        equ = eval('Equipment.objects.get(id=equipping.' + t_type[equipment.type] + ')')
    except Equipment.DoesNotExist:
        equipping.HP = equipping.HP + equipment.HP
        equipping.MP = equipping.MP + equipment.MP
        equipping.att = equipping.att + equipment.att
        equipping.baoji = equipping.baoji + equipment.baoji
        equipping.shanghai = equipping.shanghai + equipment.shanghai
        equipping.xiaoguo = equipping.xiaoguo + equipment.xiaoguo
    except Exception as e:
        print('change equipment error', e)
    else:
        equipping.HP = equipping.HP - equ.HP + equipment.HP
        equipping.MP = equipping.MP - equ.MP + equipment.MP
        equipping.att = equipping.att - equ.att + equipment.att
        equipping.baoji = equipping.baoji - equ.baoji + equipment.baoji
        equipping.shanghai = equipping.shanghai - equ.shanghai + equipment.shanghai
        equipping.xiaoguo = equipping.xiaoguo - equ.xiaoguo + equipment.xiaoguo
        bag.equipments.add(equ)
    finally:
        exec('equipping.' + t_type[equipment.type] + '=equipment.id')
        bag.equipments.remove(equipment)
        bag.save()
        equipping.save()


@change_hao
def lift(hero: Player.objects, equipment: Equipment.objects):
    bag = Bag.objects.get(hero=hero)
    equipping = Equipping.objects.get(hero=hero)
    exec('equipping.' + t_type[equipment.type] + '=0')
    bag.equipments.add(equipment)
    equipping.HP = equipping.HP - equipment.HP
    equipping.MP = equipping.MP - equipment.MP
    equipping.att = equipping.att - equipment.att
    equipping.baoji = equipping.baoji - equipment.baoji
    equipping.shanghai = equipping.shanghai - equipment.shanghai
    equipping.xiaoguo = equipping.xiaoguo - equipment.xiaoguo
    bag.save()
    equipping.save()


def buy(hero: Player.objects, equipment: Equipment.objects):
    if hero.gold >= equipment.gold:
        hero.gold -= equipment.gold
        bag = Bag.objects.get(hero=hero)
        bag.equipments.add(equipment)
        store = Store.objects.get(hero=hero)
        eval('store.' + t_type[equipment.type] + '.remove(equipment)')
        bag.save()
        store.save()
        hero.save()
        return 'bought', equipment.gold, hero.gold
    else:
        return 'nothing', equipment.gold, hero.gold


def sale(hero: Player.objects, equipment: Equipment.objects):
    hero.gold += round(equipment.gold * 0.65)
    bag = Bag.objects.get(hero=hero)
    bag.equipments.remove(equipment)
    store = Store.objects.get(hero=hero)
    eval('store.' + t_type[equipment.type] + '.add(equipment)')
    bag.save()
    store.save()
    hero.save()
    return 'sold', round(equipment.gold * 0.65), hero.gold


def detail(request, content, res_id, name):
    if request.method == 'GET':
        admin = 'Super_Game_Admin' in request.COOKIES.keys()
        resource_type = '装备'
        if not res_id:
            resource_list = Equipment.objects.all()
        else:
            resource = Equipment.objects.get(id=res_id)
            resource = [
                ('name', '名称', resource.name),
                ('cover', '图标', '<img src="/media/' + resource.cover.name + '">'),
                ('action', '动作', '<img src="/media/' + resource.action.name + '">'),
                ('menu', '介绍', resource.menu),
                ('type', '部位', resource.type),
                ('HP', '生命值', resource.HP),
                ('MP', '法力值', resource.MP),
                ('att', '攻击力', resource.att),
                ('baoji', '暴击概率', resource.baoji),
                ('xiaoguo', '暴击效果', resource.xiaoguo),
                ('shanghai', '技能伤害加成', resource.shanghai),
                ('gold', '所需金币', resource.gold),
            ]
        return render(request, 'game/detail.html', locals())
    elif request.method == 'POST':
        resource = Equipment.objects.get(id=res_id)
        return change_content(request, name, resource)


def append(request, content):
    if request.method == 'GET':
        resource_type = '装备'
        resource = [
            ('name', '名称'),
            ('cover', '图标'),
            ('action', '动作'),
            ('menu', '介绍'),
            ('type', '部位'),
            ('HP', '生命值'),
            ('MP', '法力值'),
            ('att', '攻击力'),
            ('baoji', '暴击概率'),
            ('xiaoguo', '暴击效果'),
            ('shanghai', '技能伤害加成'),
            ('gold', '所需金币'),
        ]
        return render(request, 'game/append.html', locals())
    elif request.method == 'POST':
        resource = Equipment.objects.create(
            name=request.POST.get('name'),
            menu=request.POST.get('menu'),
            type=request.POST.get('type'),
            HP=request.POST.get('HP'),
            MP=request.POST.get('MP'),
            att=request.POST.get('att'),
            baoji=request.POST.get('baoji'),
            xiaoguo=request.POST.get('xiaoguo'),
            shanghai=request.POST.get('shanghai'),
            gold=request.POST.get('gold'),
        )
        if 'cover' in request.FILES.keys():
            resource.cover = request.FILES.get('cover')
        if 'action' in request.FILES.keys():
            resource.action = request.FILES.get('action')
        resource.save()
        return redirect('/detail/equipment/' + str(resource.id))
        # return render(request, 'game/append.html')


def delete(request, content, res_id):
    if request.method == 'GET':
        resource = Equipment.objects.get(id=res_id)
        resource.delete()
        if resource.cover.name != 'none.png':
            resource.cover.delete()
        if resource.action.name != 'none.png':
            resource.action.delete()
        return redirect('/detail/equipment/')
    elif request.method == 'POST':
        resource = {}
        for equipment in Equipment.objects.all():
            resource[equipment.id] = equipment.name
        return JsonResponse({'resource': resource})
