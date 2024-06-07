import random
import json
import datetime, time

from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text, CtxStorage

from utils.config import *
from utils.states import *
from models.user import *
from utils.keyboards import *

labeler = BotLabeler()
labeler.vbml_ignore_case = True
labeler.auto_rules = [rules.PeerRule(from_chat=False)]

@labeler.message(text=["назад"], payload={"menu":"sector"})
async def back(message: Message):
    await message.answer(text_main, keyboard=await menu_main())

@labeler.message(text=["перелёт", "обновить"], payload={"menu":"sector"})
async def info(message: Message):
    await message.answer("💬 Ищу информацию о ближайших секторах...")
    user=CtxStorage().get(message.from_id)
    x = user.sector.x
    y = user.sector.y
    result = "💬 Краткая сводка о секторах:\n\n"
    sectors = []
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if i is not x or j is not y:
                sector=SectorModel().get_or_none(x=i, y=j)
                if sector is not None:
                    sectors.append(sector)
                else:
                    sectors.append([i, j])
    for i in range(0, len(sectors)):
        result += (sectors[i].info() if isinstance(sectors[i], SectorModel) is True else f"❓Название: Отсутствует\n🌐Координаты: {sectors[i][0]}:{sectors[i][1]}\n⛏Ресурсы: Неизвестно") + '\n\n' 
    time.sleep(1.5)
    await message.answer(result, keyboard=await menu_flight(sectors))

@labeler.message(text=["назад"], payload={"menu":"flight"})
async def back(message: Message):
    await message.answer(text_sector, keyboard=await menu_sector())

@labeler.message(state=SectorState.GAME)
async def game(message: Message):
    await message.answer(f"💬 Просчитываю... Начинаю выполнять...")
    data=message.state_peer.payload["payload"]["sector"]
    time.sleep(2)
    if int(message.text) is random.randint(0, 2):
        if data[0] < data[1] - 1:
            await message.answer(f"💬 Успешный манёвр! Осталось {data[0]+1} из {data[1]}\
                                 \n\n💭 Для преодоления препядствия нужно выбрать \"1\" или \"2\"", keyboard=await menu_game())
            await state_dispenser.set(message.from_id, SectorState.GAME, payload=dict([("sector", [data[0]+1, data[1], data[2]])]))
        else: 
            user=CtxStorage().get(message.from_id)
            sector=SectorModel().create(x=user.sector.x+data[2][0], y=user.sector.y+data[2][1], opener=message.from_id)
            seconds=9000/user.ship.speed
            await state_dispenser.set(message.from_id, SectorState.WAIT, payload=dict([("time", [time.time() + seconds, sector.id])]))
            balance=data[1]*15000
            user.balance+=balance
            user.save()
            await message.answer(f"💬 Сектор открыт! Вы получили вознаграждение в размере {balance}", keyboard=await menu_main())
            await message.answer(f"💬 Перелёт займет {datetime.timedelta(seconds=seconds)}", keyboard=(Keyboard().add(Text("Обновить"), KeyboardButtonColor.PRIMARY).get_json())) 
    else:
        await message.answer(f"💬 Не удалось увернутся! Осталось {data[0]} из {data[1]}\
                             \n\n💭 Для преодоления препядствия нужно выбрать \"1\" или \"2\"", keyboard=await menu_game())

@labeler.message(text="захватить")
async def occupy(message: Message):
    user=CtxStorage().get(message.from_id)
    if user.clan is None:
        await message.answer(f"Нельзя", keyboard=await menu_sector())
        return

@labeler.message(state=SectorState.WAIT)
async def wait(message: Message):
    data = message.state_peer.payload["payload"]["time"]
    seconds = time.time()
    if(data[0] > seconds):
        await message.answer(f"💬 До прибытия: {datetime.timedelta(seconds=int(data[0] - seconds))}")
    else:
        user=CtxStorage().get(message.from_id)
        await message.answer(f"💬 Мы прилетели", keyboard=await menu_main())
        await state_dispenser.delete(message.from_id)
        user.sector=data[1]
        user.save()

@labeler.message(state=SectorState.WARP_WAIT)
async def wait(message: Message):
    data = message.state_peer.payload["payload"]["time"]
    seconds = time.time()
    if(data[0] > seconds):
        await message.answer(f"💬 До прибытия: {datetime.timedelta(seconds=int(data[0] - seconds))}")
    else:
        user=CtxStorage().get(message.from_id)
        await message.answer(f"💬 Мы прилетели", keyboard=await menu_main())
        await state_dispenser.delete(message.from_id)
        user.warp_use=time.time()+user.ship.warp_delay
        user.sector=data[1]
        user.save()

@labeler.message(payload={"menu":"warp"})
async def get_coord(message: Message):
    user=CtxStorage().get(message.from_id)
    if time.time() > user.warp_use:
        await message.answer("💬 Скажи название системы или координаты", keyboard=Keyboard(one_time=True).add(Text("Отмена")))
        await state_dispenser.set(message.from_id, SectorState.WARP)
    else:
        seconds=int(user.warp_use-time.time())
        await message.answer(f"💬 Перезагрузка варп двигателя будет длится еще: {datetime.timedelta(seconds=seconds)}", keyboard=await menu_sector())

@labeler.message(state=SectorState.WARP)
async def warp(message: Message):
    if message.text.lower() in "отмена":
        await message.answer(f"💬 Варп-прыжок отменен", keyboard=await menu_sector())
        return
    coord = message.text.split(" ")
    if len(coord) > 1:
        sector=SectorModel().get_or_none(x=int(coord[0]), y=int(coord[1]))
    else:
        sector = SectorModel().get_or_none(name=message.text)
    if sector is not None:
        user=CtxStorage().get(message.from_id)
        if sector is not user.sector:
            x=sector.x-user.sector.x
            y=sector.y-user.sector.y
            seconds=9000*int((pow(x, 2)+pow(y, 2))**0.5)/user.ship.warp_speed
            await message.answer(f"💬 Перелёт в сектор {sector.name} займет {datetime.timedelta(seconds=seconds)}", keyboard=(Keyboard().add(Text("Обновить"), KeyboardButtonColor.PRIMARY).get_json()))
            await state_dispenser.set(message.from_id, SectorState.WARP_WAIT, payload=dict([("time", [time.time() + seconds, sector.id])]))
        else:
            await message.answer(f"💬 Вы уже в этом секторе", keyboard=Keyboard(one_time=True).add(Text("Отмена")))
    else:
        await message.answer(f"💬 Такой сектор ещё неизвестен. Попробуйте ещё раз", keyboard=Keyboard(one_time=True).add(Text("Отмена")))

@labeler.message(payload_contains={"sector":"flight"})
async def start(message: Message):
    data = json.loads(message.payload)["info"]
    if message.text == "Угроза":
        lvl = (pow(int(data[0]), 2) + pow(int(data[1]), 2))
        await state_dispenser.set(message.from_id, SectorState.GAME, payload=dict([("sector", [0 , lvl, data])]))
        await message.answer(f"💬 Чтобы проложить путь к неизвестному сектору нужно преодолеть {lvl} препядствий\
                             \n\n💭 Для преодоления препядствия нужно выбрать \"1\" или \"2\"", keyboard=await menu_game())
    else:
        user=CtxStorage().get(message.from_id)
        seconds = 9000 / user.ship.speed
        x=user.sector.x+data[0]
        y=user.sector.y+data[1]
        id = SectorModel().get_or_none(x=x, y=y)
        await state_dispenser.set(message.from_id, SectorState.WAIT, payload=dict([("time", [time.time() + seconds, id])]))
        await message.answer(f"💬 Перелёт займет {datetime.timedelta(seconds=seconds)}", keyboard=(Keyboard().add(Text("Обновить"), KeyboardButtonColor.PRIMARY).get_json()))