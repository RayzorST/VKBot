from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import CtxStorage

from utils.config import *
from utils.states import *
from utils.keyboards import *
from models.user import *
from models.base import *

labeler = BotLabeler()
labeler.vbml_ignore_case = True
labeler.auto_rules = [rules.PeerRule(from_chat=False)]

@labeler.message(payload={"menu":"nav"})
async def nav(message: Message):
    await message.answer("Навигация", keyboard=await menu_sector())

@labeler.message(payload={"menu":"clanmenu"})
async def clan(message: Message):
    user=CtxStorage().get(message.from_id)
    if user.clan is not None:
        await message.answer(text_clan1, keyboard=await menu_clan1())
    else: 
        await message.answer(text_clan2, keyboard=await menu_clan2())

@labeler.message(payload={"menu":"duel"})
async def duel(message: Message):
    await message.answer(text_duel, keyboard=await menu_duel())

@labeler.message(payload={"menu":"base"})
async def base(message: Message):
    user=CtxStorage().get(message.from_id)
    bases=BaseModel().select().where(BaseModel.owner==user.id)
    text="💬 "
    count=len(bases)
    if count==0:
        text+="Ещё нет ни одной базы"
    elif count==1:
        text+=f"У Вас 1 база в секторе\n{bases[0].sector}"
    else:
        text+=f"У Вас {len(bases)} баз в секторах"
        for base in bases:
            text+=f"\n{base.sector}"
    await message.answer(text, keyboard=await menu_base())

@labeler.message(state=MiningState.WAIT)
async def resources_wait(message: Message):
    await message.answer(f"Добыча ресурсов не законченна")