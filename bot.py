import random
import flet
import time

from vkbottle import CtxStorage,BaseMiddleware
from vkbottle.bot import Message
from loguru import logger
from PIL import Image, ImageDraw, ImageFont
from threading import Thread

from utils.config import *
from handlers import labelers
from models.user import *
from utils.keyboards import *
from utils.states import *
from map import *
from utils.my_flet import web_start

logger.disable("vkbottle")

@lw.interval(hours=6)
async def generate_map():
    new_map()

class Middleware(BaseMiddleware[Message]):
    storage=CtxStorage()
    async def pre(self):
        self.storage.set(self.event.from_id, get_user(self.event.from_id))
        user=CtxStorage().get(self.event.from_id)
        if user is None and self.event.text not in ["начать", "Начать"]:
            await self.event.answer(message="У Вас нет аккаунта, чтобы создать напишите 'Начать'")
            self.stop()
        if user is not None and user.banned >= time.time():
            await self.event.answer("Вы забанены!")
            self.stop()

    async def post(self):
        if not self.handlers:
            await self.event.answer("💬 Я тебя не понимаю")

        if (await state_dispenser.get(self.event.from_id)).state in ["SectorState:1", "DuelState:1"]:
            await self.event.answer(f"💭 Совет: {random.choice(adviсe)}")

for labeler in labelers:
    bot.labeler.load(labeler)

bot.labeler.message_view.register_middleware(Middleware)

def bot_start():
    bot.run_forever()

#Thread(target=web_start).start()
Thread(target=bot_start()).start()