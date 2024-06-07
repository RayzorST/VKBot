import json

from peewee import *
from models.item import ItemModel
from utils.config import db
    
class ClanModel(Model):
    class Meta:
        database = db
        db_table = 'Clans'
        
    #meta
    id = IntegerField(null=False, primary_key=True)
    name = CharField(null=False, default="None")
    chat = CharField(null=True, default=None)
    lvl = IntegerField(null=False, default=1)
    member_count = IntegerField(null=False, default=1)
    sector_count = IntegerField(null=False, default=0)
    free = BooleanField(null=False, default=False)

    #lvl
    first = CharField(null=False, default="First")
    second = CharField(null=False, default="Second")
    third = CharField(null=False, default="Third")
    fourth = CharField(null=False, default="Fourth")
    fifth = CharField(null=False, default="Fifth")

    #settings
    free = BooleanField(null=False, default=False)
    red = SmallIntegerField(null=False, default=255)
    green = SmallIntegerField(null=False, default=255)
    blue = SmallIntegerField(null=False, default=255)

    #inventory
    balance = IntegerField(null=False, default=0)
    titan = IntegerField(null=False, default=0)
    plasma = IntegerField(null=False, default=0)
    damask = IntegerField(null=False, default=0)
    energy = IntegerField(null=False, default=0)

    def to_string(self):
        return f"💬 Вот вся информация о клане\
            \n\nНазвание: {self.name}\
            \nУровень: {self.lvl}\
            \n🆔 ID: {self.id}\
            \n📨 Чат: {f'[{self.chat}|перейти]' if self.chat is not None else '-'}\
            \n\n🟪 Титана: {self.titan}/{self.lvl*10000}\
            \n🟥 Плазмы: {self.plasma}/{self.lvl*10000}\
            \n🟩 Дамаска: {self.damask}/{self.lvl*10000}\
            \n🟨 Энергии: {self.energy}/{self.lvl*10000}"

    def add_item(self, item: int) -> bool:
        items=[]
        if self.items!="":
            items=json.loads(self.items)
        if self.lvl*5 == len(items):
            return False
        items.append(item)
        self.items=json.dumps(items)
        self.save()
        return True

    def del_item(self, item: int):
        items=[]
        if self.items!="":
            items=json.loads(self.items)
        try:
            items.remove(item)
            self.items=json.dumps(items)
            self.save()
            return True
        except:
            return False
    
    def post(self, lvl) -> str:
        if lvl == 1: return self.first
        elif lvl == 2: return self.second
        elif lvl == 3: return self.third
        elif lvl == 4: return self.fourth
        elif lvl == 5: return self.fifth
        else: return "Error"

    def settings(self) -> str:
        free=bool(self.free)
        return f"Настройки клана\
        \n\n{'🔓' if free else '🔒'} Свободный вход: {'Разрешён' if free  else 'Запрещён'}"
    
    def get_settings(self) -> []:
        return [bool(self.free), [self.red, self.green, self.blue]]
    
    def get_info(self) -> str:
        return f"{self.name} : {self.member_count}/{self.lvl*5}"