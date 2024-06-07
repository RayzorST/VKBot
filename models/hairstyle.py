from peewee import *
from utils.config import db
    
class HairstyleModel(Model):
    class Meta:
        database = db
        db_table = 'Hairstyles'

    #meta
    id = PrimaryKeyField()
    path = CharField(null=False, default="None")

    #info
    name = CharField(null=False, default="None")