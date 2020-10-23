from django.db import models


# Create your models here.
class Equipment(models.Model):
    name = models.CharField('装备名称', max_length=60, unique=True)
    cover = models.ImageField('装备图标', upload_to='equipment/img/', default='none.png')
    action = models.ImageField('装备动作', upload_to='equipment/act_gif/', default='none.png')
    menu = models.CharField('介绍', max_length=120)
    type = models.CharField('部位', max_length=6)
    gold = models.IntegerField('所需金币')

    HP = models.IntegerField('生命值')
    MP = models.IntegerField('法力值')
    att = models.IntegerField('攻击力')
    baoji = models.FloatField('暴击概率')
    xiaoguo = models.FloatField('暴击效果')
    shanghai = models.FloatField('技能伤害')
