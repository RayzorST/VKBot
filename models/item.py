from peewee import *
from utils.config import db

######### Типы вещей
# 0 Другое
# 1 Оружие
# 2 Броня
#########

choices=["Other", "Armor", "Weapon"]

class ItemModel(Model):
    class Meta:
        database = db
        db_table = 'Items'

    #meta
    id = PrimaryKeyField()
    path = CharField(null=False, default="None")
    type = TextField(null=False, choices=choices, default=choices[0])

    #info
    name = CharField(null=False, default="None")
    description = CharField(null=False, default="None")

    #armor
    helmet = BooleanField(null=False, default=False)

    #weapon