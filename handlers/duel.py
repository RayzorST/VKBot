from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import Keyboard, Text, CtxStorage

from utils.config import *
from utils.states import *
from models.user import *
from utils.keyboards import *

labeler = BotLabeler()
labeler.vbml_ignore_case = True
labeler.auto_rules = [rules.PeerRule(from_chat=False)]

@labeler.message(text=["назад"], payload={"duel":"menu"})
async def duel(message: Message):
    await message.answer(text_main, keyboard=await menu_main())