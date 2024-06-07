import random

from peewee import *
from models.clan import ClanModel
from utils.config import db

def random_name() -> str:
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
    result = ""
    l = random.randint(5, 10)
    i = 0
    while i != l:
        result+=random.choice(chars)
        i+=1
    return result

def random_type():
    return random.choice(sector_types)

sector_types=["Пустошь", "Чёрная дыра", 
              "Жёлтый карлик", "Красные карлики", 
              "Белый карлик", "Пульсар", 
              "Нейтронная", "Протозвезда", 
              "Белый гигант", "Сверхновая звезда", 
              "Двойная звезда"]
    
class SectorModel(Model):
    class Meta:
        database = db
        db_table = 'Sectors'
    #meta
    id = IntegerField(null=False, primary_key=True)

    #info
    name = CharField(null=False, default="None")
    opener = IntegerField(null=False, default=-1)
    type = CharField(null=False, choices=sector_types, default=sector_types[0])
    x = IntegerField(null=False, default=0)
    y = IntegerField(null=False, default=0)

    #clan
    level = IntegerField(null=False,default=0)
    owner = ForeignKeyField(ClanModel, null=True, default=None)

    #resources
    titan = IntegerField(null=False, default=0)
    plasma = IntegerField(null=False, default=0)
    damask = IntegerField(null=False, default=0)
    energy = IntegerField(null=False, default=0)

    def create(self,x=0, y=0, opener=-1, type: str = None, resources: bool = True):
        self.name=random_name()
        self.opener=opener
        self.x=x
        self.y=y
        self.type = (type if type is not None else random_type())
        if resources is True and self.type not in ["Чёрная дыра", "Пустошь"]:
            self.titan=random.randint(0, 50)+random.randint(0, 50)
            self.plasma=random.randint(0, 50)+random.randint(0, 50)
            self.damask=random.randint(0, 50)+random.randint(0, 50)
            self.energy=random.randint(0, 50)+random.randint(0, 50)
        self.save()
        return self
    

    def info(self):
        return f"{'🌀' if self.type in ['Чёрная дыра', 'Пустошь'] else '🔆'} Название: {self.name}\
             \n🌐 Координаты: {self.x}:{self.y}\
             \n⛏ Ресурсы: {get_resources(self.titan + self.energy + self.damask + self.plasma)}"

    def to_string(self):
        from models.user import UserModel
        
        opener=UserModel().get_or_none(self.opener)
        return f"💬 Вот вся информация о нашем секторе\
            \n\n✨ Название: {self.name}\
            \n👥 Открыл: {f"@id{opener.id} ({opener.name})" if opener is not None else "Неизвестно"}\
            \n{'🌀' if self.type in ['Чёрная дыра', 'Пустошь'] else '🔆'} Тип: {self.type}\
            \n🌐 Координаты: {self.x}:{self.y}\
            \n🛡 Клан: {self.owner.name + ' : ' + str(self.level) if self.owner is not None else 'нет'}\
            \n\n⛏ Шанс найти ресурс:\
            \n🟪 Титан: {self.titan}%\
            \n🟥 Плазма: {self.plasma}%\
            \n🟩 Дамаск: {self.damask}%\
            \n🟨 Энергия: {self.energy}%"

def get_resources(res: int) -> str:
    res /= 4
    if res == 0:
        return "Отсутсвуют"
    elif res <= 20:
        return "Дефицит"
    elif res <= 60:
        return "Умеренно"
    elif res <= 100:
        return "Изобилее"
    else:
        return "Ошибка"