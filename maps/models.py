from django.db import models

from monsters.models import Monster


# Create your models here.
class Map(models.Model):
    id = models.CharField('id', max_length=32, primary_key=True)
    name = models.CharField('地图名称', max_length=60, unique=True)
    menu = models.CharField('地图介绍', max_length=120)
    cover = models.ImageField('地图封面', upload_to='map/', default='none.png')

    floor1 = models.ManyToManyField(Monster, verbose_name='1层怪物', related_name='floor1')
    boss1 = models.OneToOneField(Monster, verbose_name='1层大怪', related_name='boos1',
                                 null=True, on_delete=models.SET_NULL)

    floor2 = models.ManyToManyField(Monster, verbose_name='2层怪物', related_name='floor2')
    boss2 = models.OneToOneField(Monster, verbose_name='2层大怪', related_name='boos2',
                                 null=True, on_delete=models.SET_NULL)

    floor3 = models.ManyToManyField(Monster, verbose_name='3层怪物', related_name='floor3')
    boss3 = models.OneToOneField(Monster, verbose_name='3层大怪', related_name='boos3',
                                 null=True, on_delete=models.SET_NULL)

    floor4 = models.ManyToManyField(Monster, verbose_name='4层怪物', related_name='floor4')
    boss4 = models.OneToOneField(Monster, verbose_name='4层大怪', related_name='boos4',
                                 null=True, on_delete=models.SET_NULL)

    floor5 = models.ManyToManyField(Monster, verbose_name='5层怪物', related_name='floor5')
    boss5 = models.OneToOneField(Monster, verbose_name='5层大怪', related_name='boos5',
                                 null=True, on_delete=models.SET_NULL)
