from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from utils.db_api import db_commands as commands


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        setting = await commands.get_bot_settings()
        if str(message.from_user.id) in setting.admin_id.split("\r\n"):
            return True
        return False
