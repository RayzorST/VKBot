import json

from peewee import *
from utils.config import db
from models.clan import ClanModel
from models.hairstyle import HairstyleModel
from models.item import ItemModel
from models.sector import SectorModel
from models.ship import ShipModel
    
class UserModel(Model):
    class Meta:
        database = db
        db_table = 'Users'
    #User
    id = IntegerField(null=True, primary_key=True)
    banned = IntegerField(null=False, default=0)
    datetime = IntegerField(null=False, default=0)

    #character
    name = CharField(null=False, default="Noname", max_length=20)
    health = IntegerField(null=False, default=100)
    sector = ForeignKeyField(SectorModel, null=False, default=2)

    #clan
    clan = ForeignKeyField(ClanModel, null=True, default=None)
    clan_lvl = IntegerField(null=False, default=1)

    #skin
    skin = IntegerField(null=False, default=1)
    sex = BooleanField(null=False, default=True)
    hairstyle = ForeignKeyField(HairstyleModel, null=False, default=1)

    #equip
    armor = ForeignKeyField(ItemModel, null=False, default=1)
    weapon = ForeignKeyField(ItemModel, null=False, default=2)
    ship = ForeignKeyField(ShipModel, null=False, default=1)

    #ship
    warp_use = IntegerField(null=False, default=0)

    #invetory
    balance = IntegerField(null=False, default=10000)
    titan = IntegerField(null=False, default=0)
    plasma = IntegerField(null=False, default=0)
    damask = IntegerField(null=False, default=0)
    energy = IntegerField(null=False, default=0)
    items = CharField(null=False, default="")

    #duel

    def to_string(self):
        return (f"💬 Вот вся информация\
        \n\n📋 Имя: {self.name}\
        \n🪪 ID: @id{self.id} ({self.id})\
        \n🛡 Клан: {self.clan.name if self.clan is not None else '-'}\
        \n🎖 Звание: {f'{self.clan.post(self.clan_lvl)}' + f' ({self.clan_lvl} ур.)' if self.clan is not None else '-'}\
        \n\n🧬 Пол: {sex(self.sex)}\
        \n❤ Здоровье: {self.health}\
        \n💰 Баланс: {balance(self.balance)}\
        \n🔫 Оружие: {self.weapon.name}\
        \n🛡 Броня: {self.armor.name}\
        \n🚀 Корабль: {self.ship.name}")
    
    def inventory(self):
        items=[]
        if self.items!="":
            items=json.loads(self.items)
        other=""
        for i in range(len(items)):
            other+=f"   {i+1}. {ItemModel().get_by_id(items[i]).name}\n"
        return (f"💬 По моим данным, у нас в трюме:\
        \n\n🟪 Титана: {self.titan}/{self.ship.max_titan}\
        \n🟥 Плазмы: {self.plasma}/{self.ship.max_plasma}\
        \n🟩 Дамаска: {self.damask}/{self.ship.max_damask}\
        \n🟨 Энергии: {self.energy}/{self.ship.max_energy}\
        \n🎒 Вещи: {len(items)}/{self.ship.max_items}\
        \n{other}")
    
    def add_item(self, item: int) -> bool:
        items=[]
        if self.items!="":
            items=json.loads(self.items)
        if self.ship.max_items == len(items):
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

def get_user(id: int) -> UserModel | None:
    try:
        return UserModel().get_by_id(id) 
    except:
        return None
    
def is_banned(id: int) ->UserModel | None:
    try:
        return UserModel().get_by_id(id).banned 
    except:
        return False
    
def exist(id: int) -> bool:
    try:
        UserModel().get(id)
        return True
    except:
        return False
    
def sex(b: bool):
    if b:
        return "Мужской"
    else:
        return "Женский"

def balance(b: int) -> str:
    count = ""
    while b >= 1000:
        count+="k"
        b /= 1000
    return f"{int(b)}{count}"
    
def get_members(id: int):
    return UserModel.select().where(UserModel.clan == id)