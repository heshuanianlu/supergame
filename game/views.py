from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.clickjacking import xframe_options_sameorigin

from consumables import views as con_views
from equipments import views as equ_views
from heroes import views as hero_views
from monsters import views as monster_views
from maps import views as map_views
from users import views as user_views

from myclass.ready.savees import ys, th, he
from myclass.main.deal import info, host, store, fight, role


# Create your views here.
def index(request):
    return render(request, 'game/index.html', locals())


def ready(request):
    if request.method == 'GET':
        ys()
        th()
        he()
        return JsonResponse({"code": "successful"})
    else:
        return JsonResponse({"code": "error"})


@xframe_options_sameorigin
def game(request, content=None):
    user_id = user_views.check_token(request)
    if user_id:
        hero_id = request.session.get('hero_id')
        if not hero_id:
            return role(request, user_id)
        else:
            if content == 'host' or not content:
                return host(request, hero_id)
            elif content == 'store':
                return store(request, hero_id)
            elif content == 'fight':
                return fight(request, hero_id)
            elif content == 'info':
                return info(request, hero_id)
            else:
                print('game content error', content)
                return host(request, hero_id)
    else:
        if request.method == 'GET':
            return render(request, 'game/game.html')
        else:
            print('game request error', request.method)
            return render(request, 'game/game.html')


def append(request, content):
    if content == 'monster':
        return monster_views.append(request, content)
    elif content == 'hero':
        return hero_views.append(request, content)
    elif content == 'map':
        return map_views.append(request, content)
    elif content == 'consumable':
        return con_views.append(request, content)
    elif content == 'equipment':
        return equ_views.append(request, content)
    else:
        return render(request, 'game/append.html', locals())


def detail(request, content, res_id, name):
    if content == 'monster':
        return monster_views.detail(request, content, res_id, name)
    elif content == 'hero':
        return hero_views.detail(request, content, res_id, name)
    elif content == 'map':
        return map_views.detail(request, content, res_id, name)
    elif content == 'consumable':
        return con_views.detail(request, content, res_id, name)
    elif content == 'equipment':
        return equ_views.detail(request, content, res_id, name)
    else:
        return render(request, 'game/detail.html', locals())


def delete(request, content, res_id):
    if content == 'monster':
        return monster_views.delete(request, content, res_id)
    elif content == 'hero':
        return hero_views.delete(request, content, res_id)
    elif content == 'map':
        return map_views.delete(request, content, res_id)
    elif content == 'consumable':
        return con_views.delete(request, content, res_id)
    elif content == 'equipment':
        return equ_views.delete(request, content, res_id)
    else:
        return JsonResponse({'content': content})


def user(request, content):
    if content == 'register':
        return user_views.register(request, content)
    elif content == 'log':
        return user_views.log(request, content)
    elif content == 'edit':
        return user_views.edit(request, content)
    elif content == 'see':
        return user_views.see(request)
    else:
        return render(request, 'game/user.html', locals())


def admin(request):
    if 'Super_Game_Admin' in request.COOKIES.keys():
        return render(request, 'game/admin.html', {'admin': 1})
    return user_views.admin(request)
