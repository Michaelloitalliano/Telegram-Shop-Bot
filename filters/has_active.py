from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from utils.db_api import db_commands as commands


class IsWork(BoundFilter):
    async def check(self, message: types.Message):
        status = await commands.get_bot_settings()
        if status.bot_status:
            return False
        else:
            return True