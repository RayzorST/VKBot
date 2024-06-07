from vkbottle import BaseStateGroup

class RegisterState(BaseStateGroup):
    SEX = 0,
    SKIN = 1,
    HAIRSTYLE = 2,
    NICKNAME = 3,

class ClanRegisterState(BaseStateGroup):
    NAME = 0,

class Clan(BaseStateGroup):
    SET_TITAN = 0,
    SET_PLASMA = 1,
    SET_DAMASK = 2,
    SET_ENERGY = 3,

class SectorState(BaseStateGroup):
    GAME = 0,
    WAIT = 1,
    WARP = 2,
    WARP_WAIT = 3,

class DuelState(BaseStateGroup):
    MOVE = 0,
    WAIT = 1,
    USER = 2,

class MiningState(BaseStateGroup):
    WAIT = 0,