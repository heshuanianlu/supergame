# Generated by Django 3.0.6 on 2020-05-18 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Monster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='怪物名称')),
                ('cover', models.ImageField(default='/none.png', upload_to='monster/img/', verbose_name='怪物图标')),
                ('action', models.ImageField(default='/none.png', upload_to='monster/act_gif/', verbose_name='怪物动作')),
                ('menu', models.CharField(max_length=120, verbose_name='介绍')),
                ('HP', models.IntegerField(verbose_name='生命值')),
                ('MP', models.IntegerField(verbose_name='法力值')),
                ('att', models.IntegerField(verbose_name='攻击力')),
                ('baoji', models.FloatField(verbose_name='暴击概率')),
                ('xiaoguo', models.FloatField(verbose_name='暴击效果')),
                ('gailv', models.FloatField(verbose_name='技能概率')),
                ('shanghai', models.FloatField(verbose_name='技能伤害')),
                ('exp', models.IntegerField(verbose_name='击杀经验值')),
                ('gold', models.IntegerField(verbose_name='击杀金币')),
                ('run', models.FloatField(verbose_name='逃跑概率')),
            ],
        ),
    ]
