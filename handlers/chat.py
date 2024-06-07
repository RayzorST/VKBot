from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import CtxStorage

labeler = BotLabeler()
labeler.vbml_ignore_case = True
labeler.auto_rules = [rules.PeerRule(from_chat=True)]

@labeler.message(text=["клан"])
async def clan(message: Message):
    user = CtxStorage().get(message.from_id)
    await message.answer(user.clan.to_string())

