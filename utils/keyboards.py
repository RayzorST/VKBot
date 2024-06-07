from vkbottle import Keyboard, KeyboardButtonColor, EMPTY_KEYBOARD, Text

#main

text_main = "💬 Открываю информационное меню...\n\
    \nПрофиль\
    \nИнвентарь\
    \nСектор"

async def menu_main() -> str:
    return (Keyboard()
    .add(Text("Профиль"), KeyboardButtonColor.PRIMARY)
    .add(Text("Инвентарь"), KeyboardButtonColor.PRIMARY)
    .add(Text("Сектор"), KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("Навигация", {"menu":"nav"}), KeyboardButtonColor.POSITIVE)
    .add(Text("База", {"menu":"base"}), KeyboardButtonColor.POSITIVE)
    .add(Text("Клан", {"menu":"clanmenu"}), KeyboardButtonColor.POSITIVE)
    #.row()
    #.add(Text("Дуэль", {"menu":"duel"}), KeyboardButtonColor.NEGATIVE)
    ).get_json()

text_admin = "Команды: \nБан <id>"

async def menu_admin() -> str:
    return (Keyboard()
    .add(Text("Кол Юзеров", {"menu":"admin"}), KeyboardButtonColor.PRIMARY)
    .add(Text("Кол Кланов", {"menu":"admin"}), KeyboardButtonColor.PRIMARY)
    .add(Text("Кол Секторов", {"menu":"admin"}), KeyboardButtonColor.PRIMARY)
    .add(Text("Кол Баз", {"menu":"admin"}), KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("Назад", {"menu":"admin"}))
    .add(Text("Выключить", {"menu":"admin"}), KeyboardButtonColor.NEGATIVE)
    .get_json())

#sector

text_sector="сектор"        

async def menu_sector() -> str:
    return (Keyboard()
    .add(Text("Карта"), KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("Перелёт", {"menu":"sector"}), KeyboardButtonColor.PRIMARY)
    .add(Text("Варп-прыжок", {"menu":"warp"}), KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("Захватить", {"menu":"clan"}), KeyboardButtonColor.NEGATIVE)
    .row()
    .add(Text("Назад", {"menu":"sector"}))
    ).get_json()

text_flight="полет" 

async def menu_flight(sectors: []) -> str:
    return (Keyboard(one_time=True)
    .add(Text(f"{sectors[2].name if not isinstance(sectors[2], list) else 'Угроза'}", {"sector":"flight", "info":[-1, 1]}), KeyboardButtonColor.POSITIVE if not isinstance(sectors[2], list) else KeyboardButtonColor.NEGATIVE)
    .add(Text(f"{sectors[4].name if not isinstance(sectors[4], list) else 'Угроза'}", {"sector":"flight", "info":[0, 1]}), KeyboardButtonColor.POSITIVE if not isinstance(sectors[4], list) else KeyboardButtonColor.NEGATIVE)
    .add(Text(f"{sectors[7].name if not isinstance(sectors[7], list) else 'Угроза'}", {"sector":"flight", "info":[1, 1]}), KeyboardButtonColor.POSITIVE if not isinstance(sectors[7], list) else KeyboardButtonColor.NEGATIVE)
    .row()
    .add(Text(f"{sectors[1].name if not isinstance(sectors[1], list) else 'Угроза'}", {"sector":"flight", "info":[-1, 0]}), KeyboardButtonColor.POSITIVE if not isinstance(sectors[1], list) else KeyboardButtonColor.NEGATIVE)
    .add(Text("Обновить", {"menu":"sector"}), KeyboardButtonColor.SECONDARY)
    .add(Text(f"{sectors[6].name if not isinstance(sectors[6], list) else 'Угроза'}", {"sector":"flight", "info":[1, 0]}), KeyboardButtonColor.POSITIVE if not isinstance(sectors[6], list) else KeyboardButtonColor.NEGATIVE)
    .row()
    .add(Text(f"{sectors[0].name if not isinstance(sectors[0], list) else 'Угроза'}", {"sector":"flight", "info":[-1, -1]}), KeyboardButtonColor.POSITIVE if not isinstance(sectors[0], list) else KeyboardButtonColor.NEGATIVE)
    .add(Text(f"{sectors[3].name if not isinstance(sectors[3], list) else 'Угроза'}", {"sector":"flight", "info":[0, 1]}), KeyboardButtonColor.POSITIVE if not isinstance(sectors[3], list) else KeyboardButtonColor.NEGATIVE)
    .add(Text(f"{sectors[5].name if not isinstance(sectors[5], list) else 'Угроза'}", {"sector":"flight", "info":[1, -1]}), KeyboardButtonColor.POSITIVE if not isinstance(sectors[5], list) else KeyboardButtonColor.NEGATIVE)
    .row()
    .add(Text("Назад", {"menu":"flight"}))
    ).get_json()

async def menu_game() -> str:
    return (Keyboard(one_time=True)
    .add(Text(1), KeyboardButtonColor.PRIMARY)
    .add(Text(2), KeyboardButtonColor.PRIMARY)
    ).get_json()

#Clan

text_clan1="меню клана"

async def menu_clan1() -> str:
    return (Keyboard()
    .add(Text("Информация", {"menu":"clan"}), KeyboardButtonColor.PRIMARY)
    .add(Text("Настройки", {"menu":"clan"}), KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("Пожертвовать", {"menu":"clan"}), KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("Назад", {"menu":"clan"}))
    .add(Text("Выйти", {"menu":"clan"}), KeyboardButtonColor.NEGATIVE)
    ).get_json()

text_clan2="Клан"

async def menu_clan2() -> str:
    return (Keyboard()
    .add(Text("Войти", {"menu":"clan"}), KeyboardButtonColor.PRIMARY)
    .add(Text("Создать клан", {"menu":"clan"}), KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("Топ", {"menu":"clan"}), KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("Назад", {"menu":"clan"}))
    ).get_json()

async def menu_clan_settings(settings: []) -> str:
    return (Keyboard()
    .add(Text("Свободный вход", {"clan":"settings"}), KeyboardButtonColor.POSITIVE if settings[0] is True else KeyboardButtonColor.NEGATIVE)
    .row()
    .add(Text("Цвет"))
    .add(Text(settings[1][0], {"clan":"settings", "color":"red"}), KeyboardButtonColor.NEGATIVE)
    .add(Text(settings[1][1], {"clan":"settings", "color":"green"}), KeyboardButtonColor.POSITIVE)
    .add(Text(settings[1][2], {"clan":"settings", "color":"blue"}), KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("Назад", {"clan":"settings"}))
    ).get_json()

text_clan_resources="Какой ресурс"

async def menu_clan_resources() -> str:
    return (Keyboard()
    .add(Text("Титан", {"clan":"resources"}), KeyboardButtonColor.PRIMARY)
    .add(Text("Плазма", {"clan":"resources"}), KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("Дамаска", {"clan":"resources"}), KeyboardButtonColor.PRIMARY)
    .add(Text("Энергия", {"clan":"resources"}), KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("Назад", {"clan":"resources"}))
    ).get_json()

async def menu_free_clans(clans: [], n: int = 0) -> str:
    clan_len = len(clans)
    return (Keyboard()
    .add(Text(f"{clans[n].name}" if n < clan_len else "-", {"clan":"choose", "info":clans[n].id if n < clan_len else -1}), KeyboardButtonColor.PRIMARY if n < clan_len else KeyboardButtonColor.SECONDARY)
    .add(Text(f"{clans[1+n].name}" if n+1 < clan_len else "-", {"clan":"choose", "info":clans[1+n].id  if n+1 < clan_len else -1}), KeyboardButtonColor.PRIMARY if n+1 < clan_len else KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text(f"{clans[2+n].name}" if n+2 < clan_len else "-", {"clan":"choose", "info":clans[2+n].id  if n+2 < clan_len else -1}), KeyboardButtonColor.PRIMARY if n+2 < clan_len else KeyboardButtonColor.SECONDARY)
    .add(Text(f"{clans[3+n].name}" if n+3 < clan_len else "-", {"clan":"choose", "info":clans[3+n].id  if n+3 < clan_len else -1}), KeyboardButtonColor.PRIMARY if n+3 < clan_len else KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text(f"{clans[4+n].name}" if n+4 < clan_len else "-", {"clan":"choose", "info":clans[4+n].id  if n+4 < clan_len else -1}), KeyboardButtonColor.PRIMARY if n+4 < clan_len else KeyboardButtonColor.SECONDARY)
    .add(Text(f"{clans[5+n].name}" if n+5 < clan_len else "-", {"clan":"choose", "info":clans[5+n].id  if n+5 < clan_len else -1}), KeyboardButtonColor.PRIMARY if n+5 < clan_len else KeyboardButtonColor.SECONDARY)
    .row()
    .add(Text("Предыдущие", {"clan":"enter", "info":n-6}), KeyboardButtonColor.POSITIVE if n != 0 else KeyboardButtonColor.NEGATIVE)
    .add(Text(f"{int(n/6+1)}/{int(clan_len/6)+1}"))
    .add(Text("Следующие", {"clan":"enter", "info":n+6}), KeyboardButtonColor.POSITIVE if n+6 <= int(clan_len) else KeyboardButtonColor.NEGATIVE)
    .row()
    .add(Text("Назад", {"clan":"enter"}))
    ).get_json()

#base

async def menu_base() -> str:
    return (Keyboard()
    .add(Text("Построить", {"base":"menu"}), KeyboardButtonColor.POSITIVE) 
    .row()
    .add(Text("Назад", {"base":"menu"}))  
    ).get_json()

#duel

text_duel="Меню дуэлей"

async def menu_duel() -> str:
    return (Keyboard()
    .add(Text("Сражение", {"menu":"duel"}))
    .row()
    .add(Text("Назад", {"menu":"duel"}))
    ).get_json()