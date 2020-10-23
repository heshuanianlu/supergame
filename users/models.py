from django.db import models

from consumables.models import Consumables
from equipments.models import Equipment
from heroes.models import Hero
from maps.models import Map


# Create your models here.
class User(models.Model):
    username = models.CharField('用户名', max_length=32, unique=True)
    password = models.CharField('密码', max_length=32)

    portrait = models.ImageField('头像', upload_to='portrait/', default='none.jpg')

    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    lasted_log = models.DateTimeField('上次登录', auto_now=True)


class Player(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='玩家')
    name = models.CharField('昵称', max_length=60)
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE, verbose_name='英雄')
    map = models.ManyToManyField(Map, verbose_name='已通关地图')

    HP = models.IntegerField('基础生命值')
    MP = models.IntegerField('基础法力值')
    att = models.IntegerField('基础攻击力')
    baoji = models.FloatField('基础暴击概率')
    xiaoguo = models.FloatField('基础暴击效果')
    shanghai = models.FloatField('基础技能伤害')

    now_HP = models.IntegerField('当前生命值', default=0)
    now_MP = models.IntegerField('当前法力值', default=0)

    exp = models.IntegerField('经验值', default=0)
    gold = models.IntegerField('金币', default=100)
    lv = models.IntegerField('等级', default=1)


class Equipping(models.Model):
    hero = models.OneToOneField(Player, verbose_name='装备者', on_delete=models.CASCADE)
    head = models.IntegerField(verbose_name='头部', null=True)
    face = models.IntegerField(verbose_name='面部', null=True)
    body = models.IntegerField(verbose_name='身体', null=True)
    back = models.IntegerField(verbose_name='背部', null=True)
    waist = models.IntegerField(verbose_name='腰部', null=True)
    arm = models.IntegerField(verbose_name='臂部', null=True)
    leg = models.IntegerField(verbose_name='腿部', null=True)
    l_hand = models.IntegerField(verbose_name='左手',  null=True)
    r_hand = models.IntegerField(verbose_name='右手', null=True)
    feet = models.IntegerField(verbose_name='足具', null=True)
    HP = models.IntegerField('装备生命值', default=0)
    MP = models.IntegerField('装备法力值', default=0)
    att = models.IntegerField('装备攻击力', default=0)
    baoji = models.FloatField('装备暴击概率', default=0)
    xiaoguo = models.FloatField('装备暴击效果', default=0)
    shanghai = models.FloatField('装备技能伤害', default=0)


class Bag(models.Model):
    hero = models.OneToOneField(Player, verbose_name='装备者', on_delete=models.CASCADE)
    equipments = models.ManyToManyField(Equipment, verbose_name='装备背包')
    consumables = models.ManyToManyField(Consumables, verbose_name='药品背包')


class Store(models.Model):
    hero = models.OneToOneField(Player, verbose_name='购买者', on_delete=models.CASCADE)
    head = models.ManyToManyField(Equipment, verbose_name='头部',
                                  related_name='re_head')
    face = models.ManyToManyField(Equipment, verbose_name='面部',
                                  related_name='re_face')
    body = models.ManyToManyField(Equipment, verbose_name='身体',
                                  related_name='re_body')
    back = models.ManyToManyField(Equipment, verbose_name='背部',
                                  related_name='re_back')
    waist = models.ManyToManyField(Equipment, verbose_name='腰部',
                                   related_name='re_waist')
    arm = models.ManyToManyField(Equipment, verbose_name='臂部',
                                 related_name='re_arm')
    leg = models.ManyToManyField(Equipment, verbose_name='腿部',
                                 related_name='re_leg')
    l_hand = models.ManyToManyField(Equipment, verbose_name='左手',
                                    related_name='re_l_hand')
    r_hand = models.ManyToManyField(Equipment, verbose_name='右手',
                                    related_name='re_r_hand')
    feet = models.ManyToManyField(Equipment, verbose_name='足具',
                                  related_name='re_feet')
