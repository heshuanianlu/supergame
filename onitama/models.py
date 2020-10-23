from django.db import models
from users.models import User


# Create your models here.
class Card(models.Model):
    name = models.CharField('名称', max_length=30)
    img = models.ImageField('图片')
    methods = models.CharField('走法', max_length=120)


class Score(models.Model):
    player = models.OneToOneField(User, verbose_name='玩家', on_delete=models.CASCADE)
    stone = models.IntegerField('岩石之道获胜次数')  # 吃掉
    water = models.IntegerField('流水之道获胜次数')  # 占领
    all = models.IntegerField('总场次')
    rate = models.FloatField('胜率')
