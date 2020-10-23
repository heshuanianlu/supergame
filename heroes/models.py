from django.db import models


# Create your models here.
class Hero(models.Model):
    pos = models.CharField('英雄职业', max_length=32)
    sex = models.CharField('英雄性别', max_length=12)
    menu = models.CharField('介绍', max_length=120)

    cover = models.ImageField('英雄图标', upload_to='hero/img/', default='none.png')
    action = models.ImageField('英雄动作', upload_to='hero/act_gif/', default='none.png')


class Info(models.Model):
    hero = models.OneToOneField(Hero, on_delete=models.CASCADE, verbose_name='英雄')

    max_HP = models.IntegerField('最大基础生命值')
    min_HP = models.IntegerField('最小基础生命值')

    max_MP = models.IntegerField('最大基础法力值')
    min_MP = models.IntegerField('最小基础法力值')

    max_att = models.IntegerField('最大基础攻击力')
    min_att = models.IntegerField('最小基础攻击力')

    max_baoji = models.FloatField('最大基础暴击概率')
    min_baoji = models.FloatField('最小基础暴击概率')

    max_xiaoguo = models.FloatField('最大基础暴击效果')
    min_xiaoguo = models.FloatField('最小基础暴击效果')

    max_shanghai = models.FloatField('最大基础技能伤害')
    min_shanghai = models.FloatField('最小基础技能伤害')
