from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import CtxStorage

from utils.keyboards import *

labeler=BotLabeler()
labeler.vbml_ignore_case=True
labeler.auto_rules=[rules.PeerRule(from_chat=False)]

@labeler.message(text=["назад"], payload={"base":"menu"})
async def back(message: Message):
    await message.answer(text_main, keyboard=await menu_main())