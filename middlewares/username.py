from utils.db_api import db_commands as commands

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class UpdateUsername(BaseMiddleware):
    """
   UpdateUsernameMiddleware
    """
    def __init__(self):
        super(UpdateUsername, self).__init__()

    async def on_post_message(self, message: types.Message, data: dict):
        user = await commands.select_user(message.from_user.id)
        if user:
            if user.username != f'@{message.from_user.username}':
                await commands.update_username(message.from_user.id, f'@{message.from_user.username}')