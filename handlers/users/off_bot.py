from aiogram import types
from loader import dp

from filters import IsWork


@dp.message_handler(IsWork())
async def bot_off(message: types.Message):
    await message.answer('Технические шоколадки...')
