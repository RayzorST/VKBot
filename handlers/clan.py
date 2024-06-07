import json
import random
import time

from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import CtxStorage

from utils.config import *
from utils.states import *
from models.user import *
from utils.keyboards import *

labeler=BotLabeler()
labeler.vbml_ignore_case=True
labeler.auto_rules=[rules.PeerRule(from_chat=False)]

@labeler.message(text=["назад"], payload={"clan":"enter"})
async def back(message: Message):
    await message.answer(text_clan2, keyboard=await menu_clan2())

@labeler.message(text=["войти"], payload={"menu":"clan"})
async def enter(message: Message):
    clans=ClanModel().select().where(ClanModel.free > 0)
    text=""
    for i in range(6):
        if i < len(clans):
            text+=clans[i].get_info() + "\n"
    await message.answer("Кланы с свободным входом\n"+text, keyboard=await menu_free_clans(clans))

@labeler.message(payload_contains={"clan":"choose"})
async def choose(message: Message):
    id=json.loads(message.payload)["info"]
    clan=ClanModel().get_by_id(id)
    if clan.member_count < clan.lvl*5:
        user=CtxStorage().get(message.from_id)
        user.clan=id
        user.save()
        await message.answer(text_clan1, keyboard=await menu_clan1())
    else:
        await message.answer("В клане нет свободных мест")

@labeler.message(text=["следующие"], payload_contains={"clan":"enter"})
async def next(message: Message):
    clans=ClanModel().select().where(ClanModel.free > 0)
    n=json.loads(message.payload)["info"]
    text=""
    if n <= len(clans):
        for i in range(n, n+6):
            if i < len(clans):
                text+=clans[i].get_info() + "\n"
        await message.answer("Кланы с свободным входом\n"+text, keyboard=await menu_free_clans(clans, n))
    else:
        await message.answer("Больше кланов нет")

@labeler.message(text=["предыдущие"], payload_contains={"clan":"enter"})
async def previous(message: Message):
    clans=ClanModel().select().where(ClanModel.free > 0)
    n=json.loads(message.payload)["info"]
    text=""
    if n >= 0:
        for i in range(n, n+6):
            if i < len(clans):
                text+=clans[i].get_info() + "\n"
        await message.answer("Кланы с свободным входом\n"+text, keyboard=await menu_free_clans(clans, n))
    else:
        await message.answer("Больше кланов нет")

@labeler.message(text=["выйти"], payload={"menu":"clan"})
async def exit(message: Message):
    user=CtxStorage().get(message.from_id)
    if user.clan_lvl == 5 and user.clan.member_count > 1:
        await message.answer("Вы не можете покинуть клан, передайте управление другому")
        return
    user.clan.member_count-=1
    if user.clan.member_count < 1:
        ClanModel().delete_by_id(user.clan.id)
    user.clan=None
    user.save()
    await message.answer("Вы покинули клан")
    await message.answer(text_clan2, keyboard=await menu_clan2())

@labeler.message(text=["информация"], payload={"menu":"clan"})
async def info(message: Message):
    user=CtxStorage().get(message.from_id)
    await message.answer(f"💬 Ищу информацию о клане: {user.clan.name}...")
    time.sleep(1.5)
    await message.answer(user.clan.to_string())

@labeler.message(text=["назад"], payload={"menu":"clan"})
async def back(message: Message):
    await message.answer(text_main, keyboard=await menu_main())

@labeler.message(text=["настройки"], payload={"menu":"clan"})
async def settings(message: Message):
    user=CtxStorage().get(message.from_id)
    if user.clan_lvl != 5:
        await message.answer(f"Настройки клана доступны только {user.clan.fifth}")
        return
    await message.answer(user.clan.settings(), keyboard=await menu_clan_settings(user.clan.get_settings()))

@labeler.message(text=["пожертвовать"], payload={"menu":"clan"})
async def settings(message: Message):
    await message.answer(text_clan_resources, keyboard=await menu_clan_resources())

@labeler.message(text=["создать клан"], payload={"menu":"clan"})
async def create(message: Message):
    user=CtxStorage().get(message.from_id)
    if user.balance >= 1000000:
        await message.answer("Придумай название", keyboard=Keyboard().add(Text("Отмена")))
        await state_dispenser.set(message.from_id, ClanRegisterState.NAME)
    else:
        await message.answer("Не достаточно средств")

@labeler.message(state=ClanRegisterState.NAME)
async def name(message: Message):
    await state_dispenser.delete(message.from_id)
    if message.text.lower() == "отмена":
        await message.answer(text_clan2, keyboard=await menu_clan2())
    else:
        user=CtxStorage().get(message.from_id)
        clan=ClanModel()
        clan.name = message.text
        clan.red=random.randint(0, 255)
        clan.green=random.randint(0, 255)
        clan.blue=random.randint(0, 255)
        clan.save()
        user.clan=clan
        user.clan_lvl=5
        user.balance-=1000000
        user.save()
        await message.answer("Клан создан")
        await message.answer(text_clan1, keyboard=await menu_clan1())

@labeler.message(text=["назад"], payload={"clan":"settings"})
async def back(message: Message):
    await message.answer(text_clan1, keyboard=await menu_clan1())

@labeler.message(text=["свободный вход"], payload={"clan":"settings"})
async def setting_free(message: Message):
    user=CtxStorage().get(message.from_id)
    user.clan.free = False if bool(user.clan.free) is True else True
    user.clan.save()
    await message.answer(user.clan.settings(), keyboard=await menu_clan_settings(user.clan.get_settings()))

@labeler.message(payload_contains={"clan":"invitation"})
async def accept(message: Message):
    user=CtxStorage().get(message.from_id)
    if user.clan is not None:
        await message.answer("Вы уже в клане")
        return
    clanid=json.loads(message.payload)["info"]
    clan=ClanModel().get_by_id(clanid)
    if clan.member_count >= clan.lvl*5:
        await message.answer("В клане нет свободных мест")
        return
    user.clan=clanid
    user.clan.member_count+=1
    user.clan_lvl=1
    user.save()
    await message.answer("Вы приняли приглашение")

@labeler.message(text=["назад"], payload={"clan":"resources"})
async def back(message: Message):
    await message.answer(text_clan1, keyboard=await menu_clan1())

@labeler.message(text=["титан"], payload={"clan":"resources"})
async def set_res(message: Message):
    await state_dispenser.set(message.from_id, Clan.SET_TITAN)
    await message.answer("💬 Сколько нужно отправить?", keyboard=Keyboard().add(Text("Отмена")))

@labeler.message(text=["плазма"], payload={"clan":"resources"})
async def set_res(message: Message):
    await state_dispenser.set(message.from_id, Clan.SET_PLASMA)
    await message.answer("💬 Сколько нужно отправить?", keyboard=Keyboard().add(Text("Отмена")))

@labeler.message(text=["дамаск"], payload={"clan":"resources"})
async def set_res(message: Message):
    await state_dispenser.set(message.from_id, Clan.SET_DAMASK)
    await message.answer("💬 Сколько нужно отправить?", keyboard=Keyboard().add(Text("Отмена")))

@labeler.message(text=["энергия"], payload={"clan":"resources"})
async def set_res(message: Message):
    await state_dispenser.set(message.from_id, Clan.SET_ENERGY)
    await message.answer("💬 Сколько нужно отправить?", keyboard=Keyboard().add(Text("Отмена")))

@labeler.message(state=Clan.SET_TITAN)
async def set_titan(message: Message):
    if message.text=="Отмена":
        await state_dispenser.delete(message.from_id)
        await message.answer(text_clan_resources, keyboard=await menu_clan_resources())
        return
    try:
        count=int(message.text)
        user=CtxStorage().get(message.from_id)
        if user.titan<count:
            await message.answer("У нас столько нет")
        else:
            user.titan-=count
            user.save()
            user.clan.titan+=count
            user.clan.save()
            await message.answer("Отправлено")
            await state_dispenser.delete(message.from_id)
            await message.answer(text_clan_resources, keyboard=await menu_clan_resources())
    except:
        await message.answer("Не понимаю")

@labeler.message(state=Clan.SET_PLASMA)
async def set_plasma(message: Message):
    if message.text=="Отмена":
        await state_dispenser.delete(message.from_id)
        await message.answer(text_clan_resources, keyboard=await menu_clan_resources())
        return
    try:
        count=int(message.text)
        user=CtxStorage().get(message.from_id)
        if user.plasma<count:
            await message.answer("У нас столько нет")
        else:
            user.plasma-=count
            user.save()
            user.clan.plasma+=count
            user.clan.save()
            await message.answer("Отправлено")
            await state_dispenser.delete(message.from_id)
            await message.answer(text_clan_resources, keyboard=await menu_clan_resources())
    except:
        await message.answer("Не понимаю")

@labeler.message(state=Clan.SET_DAMASK)
async def set_damask(message: Message):
    if message.text=="Отмена":
        await state_dispenser.delete(message.from_id)
        await message.answer(text_clan_resources, keyboard=await menu_clan_resources())
        return
    try:
        count=int(message.text)
        user=CtxStorage().get(message.from_id)
        if user.damask<count:
            await message.answer("У нас столько нет")
        else:
            user.damask-=count
            user.save()
            user.clan.damask+=count
            user.clan.save()
            await message.answer("Отправлено")
            await state_dispenser.delete(message.from_id)
            await message.answer(text_clan_resources, keyboard=await menu_clan_resources())
    except:
        await message.answer("Не понимаю")

@labeler.message(state=Clan.SET_ENERGY)
async def set_energy(message: Message):
    if message.text=="Отмена":
        await state_dispenser.delete(message.from_id)
        await message.answer(text_clan_resources, keyboard=await menu_clan_resources())
        return
    try:
        count=int(message.text)
        user=CtxStorage().get(message.from_id)
        if user.energy<count:
            await message.answer("У нас столько нет")
        else:
            user.energy-=count
            user.save()
            user.clan.energy+=count
            user.clan.save()
            await message.answer("Отправлено")
            await state_dispenser.delete(message.from_id)
            await message.answer(text_clan_resources, keyboard=await menu_clan_resources())
    except:
        await message.answer("Не понимаю")