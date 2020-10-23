from django.db import models


# Create your models here.
class Consumables(models.Model):
    name = models.CharField('物品名称', max_length=60, unique=True)
    cover = models.ImageField('物品图标', upload_to='consumable/', default='none.png')
    menu = models.CharField('介绍', max_length=120)
    gold = models.IntegerField('所需金币')
    method = models.TextField('调用方法', default='')
