from peewee import *
from models.sector import SectorModel
from models.user import UserModel
from utils.config import db
    
class BaseModel(Model):
    class Meta:
        database = db
        db_table = 'Bases'
        
    #meta
    id = IntegerField(null=True, primary_key=True)

    #user
    owner = ForeignKeyField(UserModel, null=True, default=None)

    #sector
    sector = ForeignKeyField(SectorModel, null=True, default=None)
    