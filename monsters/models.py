from django.db import models


# Create your models here.
class Monster(models.Model):
    name = models.CharField('怪物名称', max_length=60, unique=True)
    cover = models.ImageField('怪物图标', upload_to='monster/img/', default='/none.png')
    action = models.ImageField('怪物动作', upload_to='monster/act_gif/', default='/none.png')
    menu = models.CharField('介绍', max_length=120)

    HP = models.IntegerField('生命值')
    MP = models.IntegerField('法力值')
    att = models.IntegerField('攻击力')
    baoji = models.FloatField('暴击概率')
    xiaoguo = models.FloatField('暴击效果')
    gailv = models.FloatField('技能概率')
    shanghai = models.FloatField('技能伤害')

    exp = models.IntegerField('击杀经验值')
    gold = models.IntegerField('击杀金币')
    run = models.FloatField('逃跑概率')
