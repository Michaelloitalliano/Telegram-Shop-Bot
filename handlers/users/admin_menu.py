from loader import dp, bot

from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext

from utils.db_api import db_commands as command
from utils.create_text_message import count_product
from filters.is_admin import IsAdmin
import asyncio

from keyboards.default import shop_reset_buy, menu_start
from django_project.telegrambot.usersmanage.models import *


@dp.message_handler(IsAdmin(), Command('admin'))
async def admin_list_command_handler(msg: Message):
    await msg.answer('Список админ-команд\n'
                     '/send - создание рассылки\n'
                     '/info - информация по остаткам\n'
                     '/stat - статистика оплат\n'
                     '/add {user_id} - выдать баланс\n'
                     '/zam {user_id} - выдать замену (баланс)\n'
                     '/find - поиск расхождений по базе и логам')


@dp.message_handler(IsAdmin(), Command('send'))
async def set_state_send_handler(msg: Message, state: FSMContext):
    await msg.answer('Введите текст рассылки: ', reply_markup=shop_reset_buy())
    await state.set_state('enter_msg_send')


async def send_message_func(user_id, text):
    user = await command.get_all_user()
    count_god = 0
    for i in user:
        try:
            await bot.send_message(chat_id=i.user_id, text=text)
            count_god += 1
            await asyncio.sleep(.05)
        except:
            pass
    bad_sms = user.count() - count_god
    await bot.send_message(chat_id=user_id, text='Рассылка успешно закончена\n'
                                                 f'Количество отправленных смс: {count_god}\n'
                                                 f'Количество заблокированных смс: {bad_sms}\n'
                                                 f'Общее количество: {user.count()}\n')


@dp.message_handler(state='enter_msg_send')
async def start_send_message_handler(msg: Message, state: FSMContext):
    await state.finish()
    if msg.text != '💢Отменить':
        await msg.answer('Рассылка успешно запущена! Ожидайте отчет', reply_markup=menu_start())
        await send_message_func(msg.from_user.id, msg.text)
    else:
        await msg.answer('Действие успешно отменено')


@dp.message_handler(IsAdmin(), Command('info'))
async def info_product_handler(msg: Message):
    text_info = 'Информация по остаткам\n\n'
    for product in Product.objects.all():
            if product.subcategory.text_mode:
                text_info+=f"{product.name} | {len(product.product_this.splitlines())} шт.\n"
            else:
                text_info+=f"{product.name} | {len(LogLink.objects.filter(product=product))} шт.\n"
    await msg.answer(text_info)

