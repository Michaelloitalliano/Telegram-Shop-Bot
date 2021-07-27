from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.db_api import db_commands as commands
from keyboards.default.start_menu import menu_start
from keyboards.inline.menu_keyboards import agreement


from django_project.telegrambot.usersmanage.models import User

from re import compile

agreement_text = """Правила"""

@dp.message_handler(CommandStart(deep_link=compile(r"\d+")))
async def bot_start_deep_link(message: types.Message):
    user = await commands.add_user(user_id=message.from_user.id,
                                   username=f'@{message.from_user.username}')
    if not user.agreement:
        return await message.answer(agreement_text, reply_markup=agreement())
    text_start = await commands.get_start_text()
    if user.referral == 0 and message.from_user.id != int(message.get_args()):
        user_referral = await commands.select_user(message.get_args())
        if user_referral is None:
            return await message.answer('😡Пользователя с таким реферальным кодом не существует')
        await commands.add_referral(user_id=message.from_user.id, referral=message.get_args())
    if text_start == '':
        await message.answer('Текст не заполнен администратором', reply_markup=menu_start())
    else:
        await message.answer(text_start, reply_markup=menu_start())

@dp.callback_query_handler(text_contains='agree')
async def agree_handler(call: types.CallbackQuery):
    user = User.objects.filter(user_id=call.from_user.id).first()
    user.agreement=True
    user.save()
    await call.message.delete()
    await call.message.answer('Рады работать с вами!', reply_markup=menu_start())

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await commands.add_user(user_id=message.from_user.id,
                                   username=f'@{message.from_user.username}')
    if not user.agreement:
        return await message.answer(agreement_text, reply_markup=agreement())
    text_start = await commands.get_start_text()
    if text_start == '':
        await message.answer('Текст не заполнен администратором', reply_markup=menu_start())
    else:
        await message.answer(text_start, reply_markup=menu_start())
