import re

from vkbottle.bot import BotLabeler, Message, rules

from models.user import UserModel
from models.clan import ClanModel
from models.sector import SectorModel
from models.base import BaseModel

from utils.keyboards import *
from utils.config import *
from map import *

labeler = BotLabeler()
labeler.vbml_ignore_case = True
labeler.auto_rules = [rules.StateGroupRule(state_group=None)]

@labeler.message(text=["назад"], payload={"menu":"admin"})
async def back(message: Message):
    await message.answer(text_main, keyboard=await menu_main())

@labeler.message(text=["Кол Юзеров"], payload={"menu":"admin"})
async def users(message: Message):
    await message.answer(len(UserModel().select()))

@labeler.message(text=["Кол Кланов"], payload={"menu":"admin"})
async def clans(message: Message):
    await message.answer(len(ClanModel().select()))

@labeler.message(text=["Кол Секторов"], payload={"menu":"admin"})
async def sectors(message: Message):
    await message.answer(len(SectorModel().select()))

@labeler.message(text=["Кол Баз"], payload={"menu":"admin"})
async def bases(message: Message):
    await message.answer(len(BaseModel().select()))

@labeler.message(text=["бан", "бан <id>"])
async def ban(message: Message, id):
    if message.from_id in admin_ids:
        message.answer("Не понимаю о чем ты")
        return
    if id is None:
        message.answer("Не указан юзер")
        return
    id=re.findall(r"[0-9]+", id)[0]
    user=UserModel().get_by_id(id)
    if user is None:
        message.answer("Не такого юзера")
        return
    user.banned=True
    user.save()

@labeler.message(text=["разбан", "разбан <id>"])
async def unban(message: Message, id):
    if message.from_id in admin_ids:
        message.answer("Не понимаю о чем ты")
        return
    if id is None:
        message.answer("Не указан юзер")
        return
    id=re.findall(r"[0-9]+", id)[0]
    user=UserModel().get_by_id(id)
    if user is None:
        message.answer("Не такого юзера")
        return
    user.banned=False
    user.save()

@labeler.message(text=["выключить"], payload={"menu":"admin"})
async def off(message: Message):
    await message.answer("Бот выключен")

@labeler.message(text=["адм карта"])
async def map(message: Message):
    new_map()
    photo = await photo_uploader.upload(
        file_source="assets/other/map.png",
        peer_id=message.peer_id,
    )
    await message.answer(attachment=photo)
