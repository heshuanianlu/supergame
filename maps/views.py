import random

from django.http import JsonResponse
from django.shortcuts import render, redirect

from maps.models import Map
from monsters.models import Monster
from myclass.main.content import change_content


# Create your views here.
def random_mon(floor: int, map: Map.objects) -> Monster.objects:
    floor = floor // 20 + 1
    mon = random.choice(eval('map.floor' + str(floor) + '.all()'))
    return mon


def check_n(floor: int, map: Map.objects) -> str or None:
    if floor == 100:
        return map.id + '_boss'
    elif 0 < floor < 100:
        if floor % 20 == 0:
            return floor//20+1, random_mon(floor, map)
        else:
            return 0, random_mon(floor, map)
    else:
        print('floor error', floor)
        return check_n(0, map)


def detail(request, content, res_id, name):
    if request.method == 'GET':
        admin = 'Super_Game_Admin' in request.COOKIES.keys()
        resource_type = '地图'
        if not res_id:
            resource_list = Map.objects.all()
        else:
            resource = Map.objects.get(id=res_id)
            resource = [
                ('id', '代号', resource.id),
                ('name', '名称', resource.name),
                ('menu', '介绍', resource.menu),
                ('cover', '图标', '<img src="/media/' + resource.cover.name + '">'),
                ['floor1', '一层怪物', resource.floor1.all()],
                ['floor2', '二层怪物', resource.floor2.all()],
                ['floor3', '三层怪物', resource.floor3.all()],
                ['floor4', '四层怪物', resource.floor4.all()],
                ['floor5', '五层怪物', resource.floor5.all()],
            ]
            for i in range(len(resource)):
                if resource[i][0][:5] == 'floor':
                    res = []
                    for j in resource[i][2]:
                        res.append(j.name)
                    resource[i][2] = '、'.join(res)
                    del res
        return render(request, 'game/detail.html', locals())
    elif request.method == 'POST':
        resource = Map.objects.get(id=res_id)
        return change_content(request, name, resource)


def append(request, content):
    if request.method == 'GET':
        resource_type = '地图'
        resource = [
            ('id', '代号'),
            ('name', '名称'),
            ('menu', '介绍'),
            ('cover', '图标'),
            ['floor1', '一层怪物'],
            ['floor2', '二层怪物'],
            ['floor3', '三层怪物'],
            ['floor4', '四层怪物'],
            ['floor5', '五层怪物'],
        ]
        return render(request, 'game/append.html', locals())
    elif request.method == 'POST':
        resource = Map.objects.create(
            id=request.POST.get('id'),
            name=request.POST.get('name'),
            menu=request.POST.get('menu'),
        )
        if 'cover' in request.FILES.keys():
            resource.cover = request.FILES.get('cover')

        for i in range(1, 6):
            value = request.POST.getlist('floor'+str(i))
            print(value)
            for v in value:
                exec('resource.floor' + str(i) + '.add(Monster.objects.get(id=v))')
        resource.save()
        return redirect('/detail/map/' + str(resource.id))
        # return render(request, 'game/append.html')


def delete(request, content, res_id):
    if request.method == 'GET':
        resource = Map.objects.get(id=res_id)
        resource.delete()
        if resource.cover.name != 'none.png':
            resource.cover.delete()
        return redirect('/detail/map/')
    elif request.method == 'POST':
        resource = {}
        for map in Map.objects.all():
            resource[map.id] = map.name
        return JsonResponse({'resource': resource})
