from peewee import *
from utils.config import db

class ShipModel(Model):
    class Meta:
        database = db
        db_table = 'Ships'
    #meta
    id = PrimaryKeyField()

    #info
    name = CharField(null=False, default="None")
    description = CharField(null=False, default="None")
    speed = IntegerField(null=False, default=100)

    #warp
    warp_speed = IntegerField(null=False, default=100)
    warp_delay = IntegerField(null=False, default=300)

    #invetory
    max_titan = IntegerField(null=False, default=100)
    max_plasma = IntegerField(null=False, default=100)
    max_damask = IntegerField(null=False, default=100)
    max_energy = IntegerField(null=False, default=100)
    max_items = IntegerField(null=False, default=4)

    def to_string(self):
        return f"{self.name}\n{self.speed}\n{self.warp_speed}\n{self.warp_delay}\n{self.description}"