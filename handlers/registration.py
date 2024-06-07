import time, datetime

from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text, CtxStorage

from utils.config import *
from utils.states import *
from utils.keyboards import *
from models.user import *

labeler = BotLabeler()
labeler.vbml_ignore_case = True
labeler.auto_rules = [rules.PeerRule(from_chat=False)]

@labeler.message(text=["начать", "/начать"])
async def start(message: Message):
    if exist(message.from_id):
        await message.answer("Начать что?")
    else:
        UserModel.create(id=message.from_id, datetime=time.time())
        await message.answer("💬 О-о...")
        time.sleep(1)
        await message.answer("💬 Хоть кого-то смог я найти на этой планете!\
                             \nТак, Я, призрак - раузмный робот, создан помогать, а создатель мой:")
        time.sleep(1)
        await message.answer("💬 А... этот фрагмент памяти поврежден.\
                             \nЛадно, сейчас мой сканер немного поврежден, ты какого пола?", keyboard=Keyboard(one_time=True)
                            .add(Text("Мужской"))
                            .add(Text("Женский")))
        await state_dispenser.set(message.from_id, RegisterState.SEX)

@labeler.message(state=RegisterState.SEX)
async def sex(message: Message):
    text=message.text.lower()
    user=CtxStorage().get(message.from_id)
    if text in ["мужской", "женский"]:
        if text=="мужской":
            user.sex=True
        else:
            user.sex=False
        user.save()
        await message.answer("Цвет кожи", keyboard=(
            Keyboard(one_time=True)
            .add(Text("1"))
            .add(Text("2"))
            .add(Text("3"))))
        await state_dispenser.set(message.from_id, RegisterState.SKIN)
    else:
        await message.answer("Что?")

@labeler.message(state=RegisterState.SKIN)
async def skin(message: Message):
    if message.text in ("1", "2", "3"):
        user=CtxStorage().get(message.from_id)
        user.skin=int(message.text)
        user.save()
        await message.answer("Волосы", keyboard=(
            Keyboard(one_time=True)
            .add(Text("1"))
            .add(Text("2"))
            .add(Text("3"))))
        await state_dispenser.set(message.from_id, RegisterState.HAIRSTYLE)
    else:
        await message.answer("Что?")

@labeler.message(state=RegisterState.HAIRSTYLE)
async def hairstyle(message: Message):
    if message.text in ("1", "2", "3"):
        user=CtxStorage().get(message.from_id)
        user.hairstyle=int(message.text)
        user.save()
        await message.answer("Имя")
        await state_dispenser.set(message.from_id, RegisterState.NICKNAME)
    else:
        await message.answer("Не понимаю")

@labeler.message(state=RegisterState.NICKNAME)
async def nickname(message: Message):
    if len(message.text) < 5:
        await message.answer("Короткое имя")
    elif len(message.text) > 20:
        await message.answer("Длинное имя")
    else:
        user = CtxStorage().get(message.from_id)
        user.name = message.text
        user.save()
        await state_dispenser.delete(message.from_id)
        await message.answer("Готово")
        await message.answer(text_main, keyboard=await menu_main())