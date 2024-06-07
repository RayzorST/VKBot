from utils.config import db
from models.user import UserModel
from models.base import BaseModel
from models.sector import SectorModel
from models.clan import ClanModel
from models.hairstyle import HairstyleModel
from models.item import ItemModel
from models.ship import ShipModel

if __name__ == "__main__":
    db.create_tables([UserModel, BaseModel, ClanModel, SectorModel, HairstyleModel, ItemModel, ShipModel])

    SectorModel().create(type="Чёрная дыра", resources=False)
    SectorModel().create(x=1, type="Жёлтый карлик")

    HairstyleModel().create()
    HairstyleModel().create()
    HairstyleModel().create()

    ItemModel().create(helmet=False, type="Armor", name="Нейро-Скай", description="def")

    ItemModel().create(name="X-23", type="Weapon", description="def")

    ShipModel().create(name="Скаут", description="Нет", speed=30)


