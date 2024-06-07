from vkbottle import API, BuiltinStateDispenser, Bot, LoopWrapper, PhotoMessageUploader
from vkbottle.bot import BotLabeler
from peewee import SqliteDatabase

token = 'vk1.a.rman4QFCeyiuJ4IG85STOzfZEML2r3kv7j5ziI-_kISZqPw8MQzMgr2lVfBqYcVpvFxSxAjd4NRoONdRUTZe4JKdMlLPGc6_sN6IbWD3z0nc3o0CO4qhdWwdsehjSbGqwonw-AXjJBnkyw1L3Nx7tTKCIZlDFhjL50bnIf3l_h8Y-uBdn-xeQzIGRclf8Q_a-yug-bSoUSkM4fyfrh9GKw'
api = API(token)
admin_ids = [322405899]
labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()
lw = LoopWrapper()
photo_uploader = PhotoMessageUploader(api)
bot = Bot(api=api, labeler=labeler, state_dispenser=state_dispenser, loop_wrapper=lw)
db = SqliteDatabase('database.db')
adviсe = ["Чем дальше от центра Вы открываете сектор - тем больше будет вознаграждение, но и больше сложность"]
