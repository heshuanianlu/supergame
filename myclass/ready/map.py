from maps.models import Map
from monsters.models import Monster


def ma():
    tower1 = {1: '猫妖', 2: '猪妖', 3: '熊孩子', 4: '史莱姆', 5: '蜂窝', 6: '小偷'}
    tower2 = {1: '歌姬', 2: '食人花', 3: '小偷', 4: '史莱姆', 5: '哥布林', 6: '刺客'}
    tower3 = {1: '刺客', 2: '歌姬', 3: '舞女', 4: '骑士', 5: '大人物的保镖', 6: '佣兵'}
    tower4 = {1: '大人物的保镖', 2: '大人物', 3: '骑士', 4: '克隆怪物', 5: '宝箱怪', 6: '老前辈'}
    tower5 = {1: '三头犬', 2: '虚无之壁', 3: '三只狗', 4: '大人物', 5: '魔鬼', 6: '老前辈'}

    forest1 = {1: '史莱姆', 2: '野猪', 3: '熊孩子', 4: '哥布林', 5: '花妖',
               6: '树精', 7: '两只野猪', 8: '石妖', 9: '佣兵'}
    forest2 = {1: '大哥布林', 2: '矮人', 3: '地精', 4: '佣兵', 5: '树精',
               6: '小哥布林', 7: '两只野猪', 8: '食人花', 9: '佣兵队长'}
    forest3 = {1: '地精', 2: '巨人', 3: '小哥布林', 4: '宝箱怪', 5: '老前辈',
               6: '矮人王', 7: '科学家', 8: '克隆怪物', 9: '科学家'}
    forest4 = {1: '巨人', 2: '矮人王', 3: '大哥布林', 4: '四不像', 5: '老前辈',
               6: '被感染的哥布林', 7: '克隆怪物', 8: '科学家', 9: '魔鬼'}
    forest5 = {1: '四不像', 2: '巨人首领', 3: '魔鬼', 4: '佣兵队长', 5: '老前辈',
               6: '哥布林皇帝', 7: '哥布林皇后', 8: '被感染的哥布林', 9: '魔鬼'}

    menu = {'tower': '这是一座高塔，有神秘人住在其中',
            'forest': '森林被污染了，是谁这么干的'}

    for r, n in {'tower': '高塔', 'forest': '森林'}.items():
        m = Map.objects.create(name=n, id=r)
        for j in range(1, 6):
            for _, i in eval(r+str(j)+'.items()'):
                eval('m.floor'+str(j)+'.add(Monster.objects.get(name=i))')
        m.save()
