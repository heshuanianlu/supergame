import random

from consumables.models import Consumables
from consumables.views import use_co
from monsters.models import Monster
from users.models import Player, Equipping


class Action(object):
    def __init__(self):
        pass

    @staticmethod
    def BJ(damage, baoji, shanghai):
        if random.random() <= baoji:
            damage = round(damage * shanghai)
            baoji = 1
        else:
            damage = round(damage)
            baoji = 0
        return damage, baoji

    def GJ(self, att, baoji, shanghai):
        damage = self.BJ(att, baoji, shanghai)
        return damage, 0

    def JN(self, att, xiaoguo, mp, baoji, shanghai):
        if mp >= 10:
            damage = self.BJ(att * xiaoguo, baoji - 0.1, shanghai)
            return damage, 1
        else:
            damage = self.GJ(att, baoji, shanghai)
            return damage

    @staticmethod
    def FY(damage):
        damage = damage // 10 + 1
        return damage

    @staticmethod
    def TP(run):
        if random.random() <= run:
            return True

    @staticmethod
    def YN(hero: Player.objects, co: str):
        co = Consumables.objects.get(name=co)
        use_co(hero, co)

    @staticmethod
    def death(hp):
        if hp <= 0:
            return True


class Fight(object):
    def __init__(self, hero: Player.objects, monster: Monster.objects,
                 mon_HP: int, mon_MP: int, action: str, vary: int = 0):
        self.hero = hero
        self.equ = Equipping.objects.get(hero=hero)
        self.mon_HP = mon_HP
        self.mon_MP = mon_MP
        self.hero_damage = 0
        self.mon_damage = 0
        self.action = action[0:2]
        if self.action != action:
            self.con = action[2:]
        self.run = False
        self.hero_jineng = self.hero_baoji = self.mon_jineng = self.mon_baoji = 0
        self.result = [('continue', 0, 0)]

        if type(monster) is dict:
            print(vary)
            self.ms_att = monster['att']
            self.ms_baoji = monster['baoji']
            self.ms_xiaoguo = monster['xiaoguo']
            self.ms_shanghai = monster['shanghai']
            self.ms_gailv = monster['gailv']
            self.ms_run = 0
            self.ms_exp = 10000
            self.ms_gold = 10000
        elif vary:
            self.ms_att = monster.att * 0.7 * (vary + 1)
            self.ms_baoji = monster.baoji * (1 + 0.1 * vary)
            self.ms_xiaoguo = monster.xiaoguo * (2 - 0.1 * vary)
            self.ms_shanghai = monster.shanghai * (2 - 0.1 * vary)
            self.ms_gailv = monster.gailv * (1 + 0.1 * vary)
            self.ms_run = 0.01
            self.ms_exp = monster.exp * vary
            self.ms_gold = monster.gold * vary
        else:
            self.ms_att = monster.att
            self.ms_baoji = monster.baoji
            self.ms_xiaoguo = monster.xiaoguo
            self.ms_shanghai = monster.shanghai
            self.ms_gailv = monster.gailv
            self.ms_run = monster.run
            self.ms_exp = monster.exp
            self.ms_gold = monster.gold

    def hero_cause_damage(self):
        if self.action == 'GJ':
            ((self.hero_damage, self.hero_baoji), self.hero_jineng) = Action().GJ(
                self.hero.att + self.equ.att,
                self.hero.baoji + self.equ.baoji,
                self.hero.shanghai + self.equ.shanghai
            )
        elif self.action == 'JN':
            ((self.hero_damage, self.hero_baoji), self.hero_jineng) = Action().JN(
                self.hero.att + self.equ.att,
                self.hero.xiaoguo + self.equ.xiaoguo,
                self.hero.now_MP,
                self.hero.baoji + self.equ.baoji,
                self.hero.shanghai + self.equ.shanghai
            )
            if self.hero.now_MP >= 10:
                self.hero.now_MP -= 10
        elif self.action == 'TP':
            self.run = Action.TP(self.ms_run)
        elif self.action == 'YN':
            Action.YN(self.hero, self.con)

    def hero_defence_damage(self):
        self.mon_damage = Action.FY(self.mon_damage)

    def mon_cause_damage(self):
        if random.random() <= self.ms_gailv:
            ((self.mon_damage, self.mon_baoji), self.mon_jineng) = Action().JN(
                self.ms_att,
                self.ms_xiaoguo,
                self.mon_MP,
                self.ms_baoji,
                self.ms_shanghai
            )
        else:
            ((self.mon_damage, self.mon_baoji), self.mon_jineng) = Action().GJ(
                self.ms_att,
                self.ms_baoji,
                self.ms_shanghai
            )

    def mon_defence_damage(self):
        self.hero_damage = Action.FY(self.hero_damage)

    def damage(self):
        if self.run:
            exp = round(self.hero.exp / 2)
            if self.hero.exp < exp:
                self.hero.exp = 0
            else:
                self.hero.exp -= exp
            self.result[0] = ('run', 0, exp)
        else:
            self.mon_HP -= self.hero_damage
            if Action.death(self.mon_HP):
                self.hero.gold += self.ms_gold
                self.hero.exp += self.ms_exp
                self.result[0] = ('victory', self.ms_gold, self.ms_exp)
                return
            self.hero.now_HP -= self.mon_damage
            if Action.death(self.hero.now_HP):
                self.hero.now_HP = self.hero.HP + self.equ.HP
                self.hero.now_MP = self.hero.MP + self.equ.MP
                self.hero.gold -= round(self.ms_gold / 2)
                if self.hero.gold < 0:
                    self.hero.gold = 0
                self.result[0] = ('defeated', round(self.ms_gold / 2), 0)

    def fight(self) -> [
        (str, int, int),
        (int, bool, bool),
        (int, bool, bool),
    ]:
        """
        第一步：计算双方伤害
        第二步：计算减免伤害
        第三步：造成伤害
        第四步：计算死亡
        第五步：进行结算
        (
        (zhuangtai, gold, exp),
        (hero_damage, hero_baoji, hero_jineng),
        (mon_damage, mon_baoji, mon_jineng),
        )
        """
        mon_action = random.random() <= self.ms_run
        hero_action = self.action == 'FY'
        if hero_action and mon_action:
            self.result[0] = ('defence', 0, 0)
        elif hero_action:
            self.mon_cause_damage()
            self.hero_defence_damage()
        elif mon_action:
            self.result[0] = ('defense', 0, 0)
            self.hero_cause_damage()
            self.mon_defence_damage()
        else:
            self.hero_cause_damage()
            self.mon_cause_damage()
        self.damage()
        self.hero.save()
        self.result.append((self.hero_damage, self.hero_baoji, self.hero_jineng))
        self.result.append((self.mon_damage, self.mon_baoji, self.mon_jineng))
        return self.result


def _damage(f: tuple) -> str:
    bj = {True: '，<br>并造成了暴击', False: ''}
    jn = {True: '技能', False: '普通攻击'}
    return '使用了' + jn[f[2]] + bj[f[1]] + '，<br>造成了' + str(f[0]) + '伤害。<hr>'
