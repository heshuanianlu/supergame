import random

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from consumables import models as co_models
from equipments import models as equ_models
from equipments.views import equipe, buy, sale, lift
from heroes import models as hero_models
from heroes.views import lv_need_exp, lv_up
from monsters import models as monster_models
from monsters.views import forest_boss, tower_boss, boss_20
from maps import models as map_models
from maps.views import check_n
from myclass.main.fight import Fight, _damage
from users import models as user_models


def host(request, hero_id):
    if request.method == 'GET':
        player = user_models.Player.objects.get(id=hero_id)
        # print(player.player.portrait)
        equ = user_models.Equipping.objects.get(hero=player)
        exp = lv_need_exp(player.lv)
        HP = player.HP + equ.HP
        MP = player.MP + equ.MP
        att = player.att + equ.att
        baoji = round(player.baoji + equ.baoji, 2)
        shanghai = round(player.shanghai + equ.shanghai, 2)
        xiaoguo = round(player.xiaoguo + equ.xiaoguo, 2)
        return render(request, 'game/host.html', locals())
    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == 'exit':
            del request.session['hero_id']
        else:
            print('host action error', action)
        return JsonResponse({})
    else:
        print('host request error', request.method)
        return HttpResponseRedirect('/')


def store(request, hero_id):
    if request.method == 'GET':
        player = user_models.Player.objects.get(id=hero_id)
        store_equ = user_models.Store.objects.get(hero_id=hero_id)
        store_equ = {
            '头部装备': store_equ.head.all(),
            '面部装备': store_equ.face.all(),
            '身体装备': store_equ.body.all(),
            '臂部装备': store_equ.arm.all(),
            '左手装备': store_equ.l_hand.all(),
            '右手装备': store_equ.r_hand.all(),
            '背部装备': store_equ.back.all(),
            '腰部装备': store_equ.waist.all(),
            '腿部装备': store_equ.leg.all(),
            '足部装备': store_equ.feet.all(),
        }
        bag_equ = user_models.Bag.objects.get(hero_id=hero_id)
        bag_equ = bag_equ.equipments.all()
        return render(request, 'game/store.html', locals())
    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == 'buy':
            equ_id = request.POST.get('equ_id')
            equ = equ_models.Equipment.objects.get(id=equ_id)
            hero = user_models.Player.objects.get(id=hero_id)
            result = buy(hero, equ)
            if result[0] == 'bought':
                tip = '你购买了' + equ.name + \
                      '，花费了' + str(result[1]) + '金币' \
                                                '，你还有' + str(result[2]) + '金币'
            elif result[0] == 'nothing':
                tip = '购买' + equ.name + '失败' \
                                        '，需要' + str(result[1]) + '金币' \
                                                                 '，而你只有' + str(result[2]) + '金币'
            else:
                tip = '发生了一些错误，请重新购买'
        elif action == 'sale':
            equ_id = request.POST.get('equ_id')
            equ = equ_models.Equipment.objects.get(id=equ_id)
            hero = user_models.Player.objects.get(id=hero_id)
            result = sale(hero, equ)
            if result[0] == 'sold':
                tip = '你出售了' + equ.name + \
                      '，获得了' + str(result[1]) + '金币' \
                                                '，你还有' + str(result[2]) + '金币'
            else:
                tip = '发生了一些错误，请重新出售'
        else:
            tip = '请求动作错误'
            print('store action error', action)
        return JsonResponse({'tip': tip})
    else:
        print('store request error', request.method)
        return HttpResponseRedirect('/')


def fight(request, hero_id):
    if request.method == 'GET':
        map_id = request.GET.get('map_id')
        if map_id:
            map = map_models.Map.objects.get(id=map_id)
            content = 'monster'
        else:
            maps = map_models.Map.objects.all()
            content = 'map'
        return render(request, 'game/fight.html', locals())
    elif request.method == 'POST':
        action = request.POST.get('action')
        hero = user_models.Player.objects.get(id=hero_id)
        equ = user_models.Equipping.objects.get(hero=hero)
        if action == 'continue':
            map_id = request.POST.get('map_id')
            floor = int(request.POST.get('floor')) + 1
            monster = check_n(floor, map_models.Map.objects.get(id=map_id))
            if type(monster) is tuple:
                vary, monster = monster
                request.session['monster_id'] = monster.id
                if vary:
                    monster = boss_20(monster, vary)
                    monster = {
                        'name': monster['name'], 'menu': monster['menu'],
                        'HP': monster['HP'], 'MP': monster['MP'],
                        'att': monster['att'], 'baoji': monster['baoji'],
                        'xiaoguo': monster['xiaoguo'], 'shanghai': monster['shanghai'],
                        'img': str(monster['mon'].action),
                    }
                else:
                    monster = {
                        'name': monster.name, 'menu': monster.menu,
                        'HP': monster.HP, 'MP': monster.MP,
                        'att': monster.att, 'baoji': monster.baoji,
                        'xiaoguo': monster.xiaoguo, 'shanghai': monster.shanghai,
                        'img': str(monster.action),
                    }
            elif type(monster) is str:
                request.session['monster_id'] = monster
                monster = eval(monster + '(hero)')
                monster = {
                    'name': monster['name'], 'menu': monster['menu'],
                    'HP': monster['HP'], 'MP': monster['MP'],
                    'att': monster['att'], 'baoji': monster['baoji'],
                    'xiaoguo': monster['xiaoguo'], 'shanghai': monster['shanghai'],
                    'img': '/none/none.jpg',
                    # 'img': str(monster['boss_gif']),
                }
            else:
                print('monster is None')
                return JsonResponse({"code": 0})
            hero = {
                'name': hero.name, 'menu': hero.hero.menu,
                'HP': hero.HP + equ.HP, 'MP': hero.MP + equ.MP,
                'now_HP': hero.now_HP, 'now_MP': hero.now_MP,
                'att': hero.att + equ.att, 'baoji': hero.baoji + equ.baoji,
                'xiaoguo': hero.xiaoguo + equ.xiaoguo, 'shanghai': hero.shanghai + equ.shanghai,
                'img': str(hero.hero.action),
            }
            return JsonResponse({'code': 1, 'monster': monster, 'hero': hero})
        if action == 'gohost':
            hero.now_HP += round((hero.HP + equ.HP - hero.now_HP) * hero.lv / 100)
            hero.now_MP += round((hero.MP + equ.MP - hero.now_MP) * hero.lv / 100)
            if hero.now_HP >= hero.HP + equ.HP:
                hero.now_HP = hero.HP + equ.HP
            if hero.now_MP >= hero.MP + equ.MP:
                hero.now_MP = hero.MP + equ.MP
            hero.save()
        elif not action:
            print('fight action error is null')
        else:
            monster_id = request.session.get('monster_id')
            if type(monster_id) is str:
                monster = eval(monster_id + '(hero)')
                monster_name = monster['name']
            elif type(monster_id) is int:
                monster = monster_models.Monster.objects.get(id=monster_id)
                monster_name = monster.name
            else:
                print('monster is None')
                return JsonResponse({"code": 0})
            mon_HP = int(request.POST.get('mon_HP'))
            mon_MP = int(request.POST.get('mon_MP'))
            floor = int(request.POST.get('floor')) // 20
            vary = floor // 20 + 1 if floor % 20 == 0 else 0
            _result, _hero, _monster = Fight(
                hero=hero, monster=monster,
                mon_HP=mon_HP, mon_MP=mon_MP,
                action=action, vary=vary
            ).fight()
            # print(_result)

            other = ''
            if _result[0] == 'run':
                introduce = '你失去了' + str(_result[2]) + '经验！<br>成功逃脱了' \
                            + monster_name + '的魔爪！'
            elif _result[0] == 'defence':
                introduce = '你和' + monster_name + '都默契的进行了防御！<br>本回合都未造成伤害！'
            elif _result[0] == 'victory':
                introduce = '你' + _damage(_hero) + '你胜利了！<hr>' \
                            + '你获得了' + str(_result[1]) + '金币和' + str(_result[2]) + '经验！'
                exp = lv_up(hero)
                if exp[0]:
                    introduce += '<hr>你成功升级了，现在等级' + str(hero.lv) \
                                 + '.<br>距离升级还差' + str(exp[1]) + '经验。'
                    other = {
                        'att': round(hero.att + equ.att),
                        'baoji': round(hero.baoji + equ.baoji, 2),
                        'shanghai': round(hero.shanghai + equ.shanghai, 2),
                        'xiaoguo': round(hero.xiaoguo + equ.xiaoguo, 2),
                    }
            elif _result[0] == 'defeated':
                if action == 'TP':
                    introduce = '你尝试逃跑，但是失败了！<hr>'
                else:
                    introduce = '你' + _damage(_hero)
                introduce += monster_name + _damage(_monster) + '你死亡了！<hr>' \
                             + '你损失了' + str(_result[1]) + '金币！'
            elif _result[0] == 'continue':
                if action == 'TP':
                    introduce = '你尝试逃跑，但是失败了！<hr>' \
                                + monster_name + _damage(_monster) + '战斗还在继续！'
                elif action == 'FY':
                    introduce = '你进行了防御！<hr>' \
                                + monster_name + _damage(_monster) + '战斗还在继续！'
                else:
                    introduce = '你' + _damage(_hero) \
                                + monster_name + _damage(_monster) + '战斗还在继续！'
            elif _result[0] == 'defense':
                introduce = '怪物进行了防御！<hr>' \
                            + '你' + _damage(_hero) + '战斗还在继续！'
            else:
                introduce = '战斗时发生了一丝莫名其妙的错误，本回合战斗作废了！'
            mon_HP = mon_HP - _hero[0]
            mon_MP = mon_MP - _monster[2] * 10
            hero_HP = hero.now_HP
            hero_MP = hero.now_MP
            return JsonResponse({
                'monster': {'HP': mon_HP, 'MP': mon_MP},
                'hero': {'HP': hero_HP, 'MP': hero_MP},
                'introduce': introduce,
                'other': other,
                'result': _result[0]
            })
        return JsonResponse({})
    else:
        print('fight request error', request.method)
        return HttpResponseRedirect('/')


def info(request, hero_id):
    if request.method == 'GET':
        player = user_models.Player.objects.get(id=hero_id)
        equ_ing = user_models.Equipping.objects.get(hero_id=hero_id)
        HP = player.HP + equ_ing.HP
        MP = player.MP + equ_ing.MP
        att = player.att + equ_ing.att
        baoji = round(player.baoji + equ_ing.baoji, 2)
        shanghai = round(player.shanghai + equ_ing.shanghai, 2)
        xiaoguo = round(player.xiaoguo + equ_ing.xiaoguo, 2)
        equ_ing = {
            '头部装备': equ_ing.head,
            '面部装备': equ_ing.face,
            '身体装备': equ_ing.body,
            '臂部装备': equ_ing.arm,
            '左手装备': equ_ing.l_hand,
            '右手装备': equ_ing.r_hand,
            '腰部装备': equ_ing.waist,
            '背部装备': equ_ing.back,
            '腿部装备': equ_ing.leg,
            '足部装备': equ_ing.feet,
        }
        for t_equ in equ_ing:
            try:
                equ_ing[t_equ] = equ_models.Equipment.objects.get(id=equ_ing[t_equ])
            except equ_models.Equipment.DoesNotExist:
                pass
        bag_equ = user_models.Bag.objects.get(hero_id=hero_id)
        bag_equ = bag_equ.equipments.all()
        return render(request, 'game/info.html', locals())
    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == 'equipe':
            equ_id = request.POST.get('equ_id')
            equ = equ_models.Equipment.objects.get(id=equ_id)
            hero = user_models.Player.objects.get(id=hero_id)
            equipe(hero, equ)
        elif action == 'lift':
            equ_id = request.POST.get('equ_id')
            equ = equ_models.Equipment.objects.get(id=equ_id)
            hero = user_models.Player.objects.get(id=hero_id)
            lift(hero, equ)
        else:
            print('info action error', action)
        return JsonResponse({})
    else:
        print('info request error', request.method)
        return HttpResponseRedirect('/')


def role(request, user_id):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            pos = request.POST.get('pos')
            sex = request.POST.get('sex')
            name = request.POST.get('name')
            if not (pos and sex and name):
                tip = "英雄信息不完整"
            else:
                if len(user_models.Player.objects.filter(player_id=user_id)) < 3:
                    hero = hero_models.Hero.objects.get(pos=pos, sex=sex)
                    player = user_models.Player.objects.create(
                        hero=hero, name=name, player_id=user_id,
                        HP=random.uniform(hero.info.min_HP, hero.info.max_HP),
                        MP=random.uniform(hero.info.min_MP, hero.info.max_MP),
                        att=random.uniform(hero.info.min_att, hero.info.max_att),
                        baoji=random.uniform(hero.info.min_baoji, hero.info.max_baoji),
                        xiaoguo=random.uniform(hero.info.min_xiaoguo, hero.info.max_xiaoguo),
                        shanghai=random.uniform(hero.info.min_shanghai, hero.info.max_shanghai),
                    )
                    try:
                        sto = user_models.Store.objects.create(hero=player)
                        user_models.Equipping.objects.create(hero=player)
                        user_models.Bag.objects.create(hero=player)
                        for e in ['这是帽子', '这是衣服', '这是鞋子',
                                  '这是披肩', '这是裤子', '这是盾', '这是剑']:
                            equipe(player, equ_models.Equipment.objects.get(name=e))
                        equ = user_models.Equipping.objects.get(hero=player)
                        player.now_HP = player.HP + equ.HP
                        player.now_MP = player.MP + equ.MP
                        for p, el in {
                            'head': ['一见发财', '天下太平', '绝代佳人',
                                     '灭法巫师之帽', '牛头', '马面', '朝阳',
                                     '发鞭', '丝袜', '纸盒',
                                     '头盔', '皮皮熊头套'],
                            'face': ['泣血之殇', '日月璀璨', '噙者之面',
                                     '星云面甲', '焚月之镜', '灼阳之眼', '变身面具',
                                     '折磨', '狗嘴', '象牙',
                                     '口罩', '皮皮熊眼镜'],
                            'body': ['脾甲', '肝盾', '倒福',
                                     '霓裳羽衣', '黎明', '汉服', '洛丽塔',
                                     '云', '胸甲', '珠有泪',
                                     '毯子', '皮皮熊衣服'],
                            'back': ['安胃之枕', '肺眠', '招魂幡',
                                     '气冲斗牛', '黄昏', '沉鱼落雁', '闭月羞花',
                                     '风', '背甲', '玉生烟',
                                     '单子', '皮皮熊披风'],
                            'waist': ['兜率鞭', '八卦盘', '裂股之枪',
                                      '哀转', '落霞', '上清酒壶', '夕阳',
                                      '腰刀', '腰鼓', '热水瓶',
                                      '腰带', '皮皮熊腰带'],
                            'arm': ['乱世功臣', '四季肘', '游无穷',
                                    '冬梅缀', '夏落水', '秋果胚', '春花蕊',
                                    '山', '臂甲', '田日暖',
                                    '护肘', '皮皮熊袖套'],
                            'leg': ['天地之正', '四方膝', '边域将领',
                                    '东逝水', '南木灰', '西沙堆', '北雪飞',
                                    '河', '腿甲', '海月明',
                                    '护膝', '皮皮熊裤子'],
                            'l_hand': ['比心之刃', '破髓鞭', '明肾双刀之左',
                                       '长天', '空间魔方', '铁马', '国色',
                                       '姜', '流星', '鲲盾',
                                       '左护腕', '皮皮熊传单'],
                            'r_hand': ['幻脑之杖', '断肠剑', '明肾双刀之右',
                                       '秋水', '时间转盘', '冰河', '天香',
                                       '葱', '零落', '鹏枪',
                                       '右护腕', '皮皮熊拐杖'],
                            'feet': ['双飞鸳鸯', '碧玉赤足', '六气之辩',
                                     '空谷幽兰', '孤鹜', '入梦', '倾国倾城',
                                     '蒜', '沧海', '鲲鹏足具',
                                     '滑板鞋', '皮皮熊鞋子'],
                        }.items():
                            for e in el:
                                eval('sto.' + p + '.add(equ_models.Equipment.objects.get(name=e))')
                        sto.save()
                        player.save()
                    except Exception as e:
                        print('create new role error', e)
                        player.delete()
                        tip = '创建失败'
                    else:
                        tip = "创建成功"
                else:
                    tip = "英雄数目达到最大"
        elif action == 'delete':
            hero_id = request.POST.get('hero_id')
            if not hero_id:
                tip = "英雄信息不完整"
            else:
                try:
                    player = user_models.Player.objects.get(player_id=user_id, id=hero_id)
                except user_models.Player.DoesNotExist:
                    tip = "查找不到该英雄"
                except Exception as e:
                    print('delete error', e)
                    tip = "未知错误"
                else:
                    player.delete()
                    tip = "删除成功"
        elif action == 'enter':
            hero_id = request.POST.get('hero_id')
            if not hero_id:
                tip = "英雄信息不完整"
            else:
                request.session['hero_id'] = hero_id
                tip = "进入游戏"
        else:
            tip = "请求动作错误"
            print('role action error', action)
        return JsonResponse({"tip": tip})
    else:
        print('role request error', request.method)
    heroes = hero_models.Hero.objects.all()
    heroes_created = user_models.Player.objects.filter(player_id=user_id)
    return render(request, 'game/role.html', locals())
