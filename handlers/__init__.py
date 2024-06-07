from . import registration, chat, command, menu, sector, clan, admin, base

labelers = [registration.labeler, chat.labeler, command.labeler, menu.labeler, sector.labeler, clan.labeler, admin.labeler, base.labeler]

__all__ = ["labelers"]
