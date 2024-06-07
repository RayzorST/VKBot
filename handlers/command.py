import json
import random
import time
import re

from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import CtxStorage

from models.user import *
from utils.keyboards import *
from utils.config import *
from utils.states import *

labeler = BotLabeler()
labeler.vbml_ignore_case = True
labeler.auto_rules = [rules.StateGroupRule(state_group=None)]

@labeler.message(text=["инвентарь"])
async def inventory(message: Message):
    user = CtxStorage().get(message.from_id)
    await message.answer("💬 Выполняю сканирование грузового отсека...")
    time.sleep(1.5)
    await message.answer(user.inventory())

@labeler.message(text=["я", "z", "профиль"])
async def me(message: Message):
    user = CtxStorage().get(message.from_id)
    await message.answer("💬 Ищу информацию о тебе...")
    time.sleep(1.5)
    await message.answer(user.to_string(), keyboard=(Keyboard(inline=True)
        .add(Text(user.weapon.name, {"weapon":"info", "info":user.weapon.id}), KeyboardButtonColor.NEGATIVE)
        .add(Text(user.armor.name, {"armor":"info", "info":user.armor.id}), KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text(user.ship.name, {"ship":"info", "info":user.ship.id}), KeyboardButtonColor.PRIMARY)))

@labeler.message(payload_contains={"weapon":"info"})
async def weapon(message: Message):
    id=json.loads(message.payload)["info"]
    print("ok")
    weapon=ItemModel().get_by_id(id)
    await message.answer(weapon.to_string())

@labeler.message(payload_contains={"armor":"info"})
async def armor(message: Message):
    id=json.loads(message.payload)["info"]
    armor=ItemModel().get_by_id(id)
    await message.answer(armor.to_string())

@labeler.message(payload_contains={"ship":"info"})
async def ship(message: Message):
    id=json.loads(message.payload)["info"]
    ship=ShipModel().get_by_id(id)
    await message.answer(ship.to_string())

""" @labeler.message(text=["дуэль", "дуэль <user>"])
async def duel(message: Message, user=None):
    if user is None:
        await message.answer("Вы не выбрали противника")
        return
    else:
        user=re.findall(r"[0-9]+", user)[0]
        userto = get_user(int(user))
        if userto is None:
            await message.answer("Такого человека нет")
        return
    #work
 """
@labeler.message(text=["пригласить", "пригласить <id>"])
async def invitation(message: Message, id=None):
    user=CtxStorage().get(message.from_id)
    if user.clan is None:
        await message.answer("Вы не в клане")
        return
    if id is None:
        await message.answer("Вы не указали получателя")
        return
    if user.clan.member_count >= user.clan.lvl*5:
        await message.answer("В клане нет свободных мест")
        return
    id=re.findall(r"[0-9]+", id)[0]
    to=get_user(int(id))
    if to is None:
        await message.answer("Такого человека нет")
        return
    if to.clan is not None:
        await message.answer("Он уже в клане")
        return
    await message.answer("Приглашение отправлено")
    await api.messages.send(int(id), message=f"💬 Нас пригласили в клан: {user.clan.name}", 
        keyboard=(Keyboard(inline=True)
        .add(Text("Принять", {"clan":"invitation", "info":user.clan.id}), KeyboardButtonColor.POSITIVE)
        .add(Text("Отклонить", {"menu":"clan"}), KeyboardButtonColor.NEGATIVE)), random_id=0)
    await api.messages.send(user_id=int(id), message="💭 Вы можете проигнорировать это сообщение", random_id=0)

@labeler.message(text=["сектор"])
async def sector(message: Message):
    user=CtxStorage().get(message.from_id)
    await message.answer("💬 Ищу информацию по нашим координатам...")
    time.sleep(1.5)
    await message.answer(user.sector.to_string(), keyboard=(Keyboard(inline=True).add(Text("Начать добычу ресурсов"), KeyboardButtonColor.PRIMARY)))

@labeler.message(text=["Майнинг", "Начать добычу ресурсов", "Продолжить добычу"])
async def resources(message: Message):
    user=CtxStorage().get(message.from_id)
    await state_dispenser.set(message.from_id, MiningState.WAIT)
    res_name=["Титан", "Плазма", "Дамаск", "Энергия"]
    res_chance=[user.sector.titan, user.sector.plasma, user.sector.damask, user.sector.energy]
    for i in range(4):
        if random.randint(1, 100) <= res_chance[i]:
            res=random.randint(1, 100)
            await message.answer(f"⛏ Найдено {res} {res_name[i]}")
            if i == 0:
                if user.titan+res > user.ship.max_titan:
                    user.titan=user.ship.max_titan
                else:
                    user.titan+=res
            elif i == 1:
                if user.plasma+res > user.ship.max_plasma:
                    user.plasma=user.ship.max_plasma
                else:
                    user.plasma+=res
            elif i == 2:
                if user.damask+res > user.ship.max_damask:
                    user.damask=user.ship.max_damask
                else:
                    user.damask+=res
            elif i == 3:
                if user.energy+res > user.ship.max_energy:
                    user.energy=user.ship.max_energy
                else:
                    user.energy+=res
        else:
            await message.answer(f"⛏ Не удалось найти {res_name[i]}")
        time.sleep(1)
    user.save()
    await message.answer(user.inventory(), keyboard=Keyboard(inline=True).add(Text("Продолжить добычу"), KeyboardButtonColor.PRIMARY))
    await state_dispenser.delete(message.from_id)

@labeler.private_message(text=["меню", "menu"])
async def menu(message: Message):
    await message.answer("меню", payload={"menu":"main"}, keyboard=await menu_main())

@labeler.message(text=["перевести", "перевести <to>", "перевести <to> <count>"])
async def transfer_money(message: Message, to=None, count=None):
    user=CtxStorage().get(message.from_id)
    if to is None or count is None:
        await message.answer("Вы не указали получателя или сколько нужно перевести")
    else:
        try:
            to=re.findall(r"[0-9]+", to)[0]
            userto = get_user(int(to))
            if userto is None:
                await message.answer("Такого человека нет")
                return
            if user.balance > int(count):
                await message.answer("Недостаточно средств")
                return
            userto.balance=-int(count)
            userto.save()
            to.balance=+int(count)
            to.save()
        except:
            await message.answer("Ошибка при переводе")

@labeler.private_message(text=["админ"])
async def menu(message: Message):
    if message.from_id in admin_ids:
        await message.answer(text_admin, keyboard=await menu_admin())
    else:
        await message.answer("Не понимаю о чем речь")

@labeler.message(text=["кик", "кик <id>"])
async def kick(message: Message, id=None):
    user=CtxStorage().get(message.from_id)
    if user.clan is None:
        await message.answer("Вы не в клане")
        return
    if user.clan_lvl != 5:
        await message.answer("Вы не лидер")
        return
    if id is None:
        await message.answer("Не выбран игрок")
        return
    id=re.findall(r"[0-9]+", id)[0]
    to=get_user(int(id))
    if to.clan != user.clan:
        await message.answer("Игрок не из вашего клана")
        return
    to.clan=None
    to.save()
    await message.answer(f"Вы кикнули {to.name}")

@labeler.message(text=["повысить", "повысить <id>"])
async def up(message: Message, id=None):
    user=CtxStorage().get(message.from_id)
    if user.clan is None:
        await message.answer("Вы не в клане")
        return
    if user.clan_lvl != 5:
        await message.answer("Вы не лидер")
        return
    if id is None:
        await message.answer("Не выбран игрок")
        return
    id=re.findall(r"[0-9]+", id)[0]
    to=get_user(int(id))
    if to.clan != user.clan:
        await message.answer("Игрок не из вашего клана")
        return
    to.clan_lvl+=1
    if to.clan_lvl==5:
        user.clan_lvl=4
        await message.answer(f"Вас понизили повысили {to.name} до {to.clan_lvl}")
    to.save()
    await message.answer(f"Вы повысили {to.name} до {to.clan_lvl}")

@labeler.message(text=["понизить", "понизить <id>"])
async def down(message: Message, id=None):
    user=CtxStorage().get(message.from_id)
    if user.clan is None:
        await message.answer("Вы не в клане")
        return
    if user.clan_lvl != 5:
        await message.answer("Вы не лидер")
        return
    if id is None:
        await message.answer("Не выбран игрок")
        return
    id=re.findall(r"[0-9]+", id)[0]
    to=get_user(int(id))
    if to.clan != user.clan:
        await message.answer("Игрок не из вашего клана")
        return
    if to.clan_lvl==1:
        await message.answer("Игрок имеет минимальный уровень")
        return
    to.clan_lvl-=1
    to.save()
    await message.answer(f"Вы понизили {to.name} до {to.clan_lvl}")

@labeler.message(text=["карта"])
async def map(message: Message):
    await message.answer("💬 Ищу актуальную карту...")
    time.sleep(1.5)
    photo = await photo_uploader.upload(
        file_source="assets/other/map.png",
        peer_id=message.peer_id,
    )
    await message.answer("💬 На данный момент карта мира выглядит так: ", attachment=photo)

@labeler.message(text=["ping"])
async def pong(message: Message):
    user=CtxStorage().get(message.from_id)
    user.add_item(1)
    await message.answer("💬 ok")

@labeler.message(text=["pong"])
async def pong(message: Message):
    user=CtxStorage().get(message.from_id)
    user.del_item(1)
    await message.answer("💬 ok")