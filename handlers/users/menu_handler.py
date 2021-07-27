# from blockcypher import from_satoshis
import blockcypher

from loader import dp, bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from keyboards.default import reset_payment_keyboard, menu_start
from keyboards.inline import create_payment_button, create_payment_callback, return_chose_payment, return_check_payment, close, fuck
from utils.bitcoin_payment import Payment, NotConfirmed, NotPaymentFound

from utils.db_api.db_commands import select_user, get_bot_settings, get_all_user_referral, update_user_balance
from utils.create_text_message import return_referral_text, return_profile_text, return_payment_text, return_zver_payment_text
from utils.qiwi_module import QSystem, FuckingCard
from utils.zverpay import ZverPay
from utils.btc_price import Price
from utils.UAH import Course

from filters.is_admin import IsAdmin

from django_project.telegrambot.usersmanage.models import *
from django.template.defaultfilters import date as djdate

from random import randint
import math
from os.path import isdir, join as join_dirs

@dp.message_handler(text='🔄Замена')
async def change_handler(message: Message, state: FSMContext):
    await state.set_state('write_log')
    await message.answer('💡Введите <b>полное название папки лог(а)ов</b> для замены:', reply_markup=reset_payment_keyboard())
# ПРОДОЛЖЕНИЕ В SHOP_PRODUCT_HANDLER.py


@dp.message_handler(text='👤Реферальная система')
async def referral_system_open(message: Message):
    count = await get_all_user_referral(message.from_user.id)
    user = await select_user(message.from_user.id)
    bot_user = await dp.bot.get_me()
    deep_link = f'https://t.me/{bot_user.username}?start={message.from_user.id}'
    if user.referral_percent is not None:
        await message.answer(return_referral_text(user.referral_percent, deep_link, count))
    else:
        settings = await get_bot_settings()
        percent = settings.referral_percent
        await message.answer(return_referral_text(percent, deep_link, count))


@dp.message_handler(text='😎Профиль')
async def profile_handler(message: Message):
    user = await select_user(message.from_user.id)
    user_id = message.from_user.id
    username = message.from_user.username
    await message.answer(return_profile_text(user_id, username, user.balance, user.count_buy))


@dp.message_handler(text='💰Пополнить баланс')
async def chose_payment_handler(message: Message):
    await message.answer('Выберите метод пополнения', reply_markup=return_chose_payment())


@dp.callback_query_handler(lambda с: с.data.startswith('pay '))
async def payment_fuck_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    system = PaySystem.objects.filter(id=call.data.split(" ")[1]).first()
    if system==None:
        return await call.answer("Платежная система временно отключена.")
    await state.set_state('wait_amount')
    text = f"Реквизиты для пополнения:\n{system.props}\n\n"\
            "Минимальный платеж 500 рублей.\n"\
            "<b>отправьте боту сумму, на которую вы хотите пополнить бота</b>, в рублях (числом).\n"\
            f"❗️ При оплате через QIWI, в комментарии к платежу добавьте ваш ID: {call.from_user.id}"
    await call.message.answer(text, reply_markup=reset_payment_keyboard())

@dp.message_handler(state='wait_amount')
async def get_amount_handler(message: Message, state: FSMContext):
    if message.text != '💰Отмена':
        amount = message.text
        if amount==None:
            return await message.answer("<b>Отправьте боту сумму (числом)</b>.\nДля отмены оплаты нажмите на кнопку ниже.")
        if not amount.isdigit():
            return await message.answer("<b>Отправьте боту сумму (числом)</b>.\nДля отмены оплаты нажмите на кнопку ниже.")
        amount = int(amount)
        if amount>25000:
            await state.finish()
            return message.answer("Сумма должна быть меньше 25000 руб. и больше 500 руб.\nПопробуйте ещё раз или нажмите кнопку отмены.")
        elif amount<500:
            await state.finish()
            return message.answer("Сумма должна быть меньше 25000 руб. и больше 500 руб.\nПопробуйте ещё раз или нажмите кнопку отмены.")
        user = await select_user(message.from_user.id)
        await state.set_state('wait_screenshot')
        await state.update_data({'amount':amount})
        return await message.answer(f"<b>Ожидаем: {amount} руб.</b>\n\nПосле отправки платежа, для зачисления средств на профиль отправьте боту <b>скриншот платежа</b> (картинкой).\nДля отмены оплаты нажмите на кнопку ниже.")
    else:
        await message.answer('Вы успешно отменили оплату', reply_markup=menu_start())
        await state.finish()

@dp.message_handler(state='wait_screenshot',content_types=['text','photo'])
async def get_screenshot_handler(message: Message, state: FSMContext):
    if message.text != '💰Отмена':
        if message.content_type!="photo":
            return await message.answer("После отправки платежа, для зачисления средств на профиль отправьте боту <b>скрин платежа с суммой</b>(картинкой), указанной в рублях (числом), <b>одним сообщением</b>.\nДля отмены оплаты нажмите на кнопку ниже.")
        data = await state.get_data()
        amount = int(data['amount'])
        if amount>25000:
            return await state.finish()
        elif amount<500:
            return await state.finish()
        user = await select_user(message.from_user.id)
        await message.answer(f"Заявка на пополнение была отправлена, ожидайте зачисления!", reply_markup=menu_start())
        await state.finish()
        await bot.send_photo("CHANNEL_ID", message.photo[-1].file_id, caption=f"{amount}\nUser: {user.username} (ID: {user.user_id})", reply_markup=fuck(user.user_id, amount))
        if user.referral != 0:
            user_referral = await select_user(user.referral)
            percent = await get_bot_settings()
            percent = percent.referral_percent
            if user_referral.referral_percent is not None:
                percent = user_referral.referral_percent
            balance_add = math.floor(amount//100*percent)
            await update_user_balance(user.referral, balance_add)
            try:
                await bot.send_message(user_id=user.referral, text=f'Отчисление за реферала: {balance_add}')
            except:
                pass
    else:
        await message.answer('Вы успешно отменили оплату', reply_markup=menu_start())
        await state.finish()


@dp.callback_query_handler(lambda x: x.data.startswith("fuck"))
async def change_call_handler(call: CallbackQuery):
    data = call.data.split(" ")
    if len(data)!=3:
        return await call.answer("Использование команды: /add(zam) {user_id} {сумма}", True)
    u = User.objects.filter(user_id=data[1]).first()
    if u==None:
        return await call.answer(f"Пользователь с ID {data[1]} не найден!", True)
    u.balance-=u.balance*2
    u.save()
    try:
        text = f"В связи с несоответствием указанной суммы для пополнения с реальным платежом, с вас взимается штраф в виде двухкратного списания баланса с профиля."
        await bot.send_message(u.user_id, text)
        await call.answer(f"Баланс плохого человека теперь {u.balance}.\nПошёл он домой!", True)
        # await call.message.delete()
    except Exception as ex:
        await call.answer(f"Кажется, пользователь заблокировал бота, баланс был уменьшен!\n{repr(ex)}", True)


@dp.callback_query_handler(text_contains='zver')
async def zver_payment_balance_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state('write_balance_zver')
    await state.update_data({"type":"ALL"})
    await call.message.answer('💡 Введите сумму пополнения в рублях (числом):', reply_markup=reset_payment_keyboard())

@dp.callback_query_handler(text_contains='zver_UA')
async def zver_payment_balance_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state('write_balance_zver')
    await state.update_data({"type":"UA"})
    await call.message.answer('💡 Введите сумму пополнения в рублях (числом):', reply_markup=reset_payment_keyboard())


@dp.message_handler(state='write_balance_zver')
async def zver_payment_handler_two(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text.isdigit():
        if float(message.text)<500:
            await message.answer('Сумма пополнения не может быть меньше 500 рублей\nПопробуйте еще раз или нажмите на кнопку отмены')
            return
        amount_rub = int(message.text)
        uah_api = Course()
        amount = uah_api.rub_uah(amount_rub)
        system = ZverPay()
        if data["type"]=="ALL":
            invoice, url = system.create_pay(amount, "RU")
        else:
            invoice, url = system.create_pay(amount, "UA")
        await message.answer('Возвращение в меню', reply_markup=menu_start())
        await message.answer(return_zver_payment_text(amount_rub), reply_markup=create_payment_button(invoice, url))
        await state.finish()
    elif message.text == '💰Отмена':
        await state.finish()
        await message.answer('Действие отменено', reply_markup=menu_start())
    else:
        await message.answer('Сумма должна быть числом больше 500\nПопробуйте еще раз или нажмите на кнопку отмены')

@dp.callback_query_handler(text_contains='qiwi')
async def payment_balance_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    qiwi_p2p = await get_qiwi()
    if qiwi_p2p==False:
        sett = await get_bot_settings()
        return await call.message.answer(sett.text_qiwi, reply_markup=close())
    await state.set_state('write_balance')
    await call.message.answer('💡 Введите сумму пополнения в Российских рублях:', reply_markup=reset_payment_keyboard())

@dp.message_handler(state='write_balance')
async def payment_handler_two(message: Message, state: FSMContext):
    if message.text.isdigit():
        # ADD
        if float(message.text)<500:
            await message.answer('Сумма пополнения Qiwi не может быть меньше 500 рублей\nПопробуйте еще раз или нажмите на кнопку отмены')
            return
        # END ADD
        qiwi_p2p = await get_qiwi()
        if qiwi_p2p==False:
            await state.finish()
            return await message.answer('Бот временно не принимает платежи', reply_markup=menu_start())
        amount = round(float(message.text)+(randint(-99,0)/100),2)
        url = f"https://qiwi.com/payment/form/31873?amountFraction={str(round(amount-int(amount),2))[2:]}&currency=RUB&extra%5B%27account%27%5D={qiwi_p2p.card_num}&amountInteger={amount}&blocked%5B0%5D=account&blocked%5B1%5D=sum"
        await message.answer('Возвращение в меню', reply_markup=menu_start())
        await message.answer(return_payment_text(qiwi_p2p, amount), reply_markup=create_payment_button(amount, url))
        await state.finish()
    elif message.text == '💰Отмена':
        await state.finish()
        await message.answer('Действие отменено', reply_markup=menu_start())
    else:
        await message.answer('Сумма должна быть числом больше 500\nПопробуйте еще раз или нажмите на кнопку отмены')

@dp.callback_query_handler(create_payment_callback.filter(name='check_pay'))
async def check_payment_handler(call: CallbackQuery, callback_data: dict):
    if "-" in callback_data.get('bill_id'):
        system = ZverPay()
        status, bill_ids = system.check_pay(callback_data.get('bill_id'))
        uah_api = Course()
        bill_ids = uah_api.uah_rub(int(bill_ids))
    else:
        qiwi_p2p = await get_qiwi()
        if qiwi_p2p==False:
            return await call.answer('Попробуйте позже', True)
        bill_ids = float(callback_data.get('bill_id'))
        status = qiwi_p2p.check_pay(bill_ids)
    user = await select_user(call.from_user.id)
    if status:
        sum = round(bill_ids)
        await update_user_balance(user_id=call.message.chat.id, balance=sum)
        await call.message.delete()
        await call.message.answer(f'✅Баланс успешно пополнен на {sum} руб')
        user = await select_user(call.from_user.id)
        Payment.objects.create(from_user=user, amount=sum, pay_id=bill_ids)
        if user.referral != 0:
            user_referral = await select_user(user.referral)
            percent = await get_bot_settings()
            percent = percent.referral_percent
            if user_referral.referral_percent is not None:
                percent = user_referral.referral_percent
            balance_add = math.floor(sum//100*percent)
            await update_user_balance(user.referral, balance_add)
            try:
                 await bot.send_message(user_id=user.referral, text=f'Отчисление за реферала: {balance_add}')
            except:
                pass
    else:
        await call.message.answer('😡Платеж не найден')

@dp.callback_query_handler(text_contains='check_payment_btc', state='check_btc')
async def approve_btc_handler(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    data = await state.get_data()
    payment = data.get('payment')
    try:
        payment.check_payment()
    except NotConfirmed:
        await call.message.answer('Транзакция найдена, но не подтверждена\nПопробуйте позже\n\nПроверять оплату можно 1 раз в 60 секунд')
        return
    except NotPaymentFound:
        await call.message.answer('Транзакция не найдена\nПроверять оплату можно 1 раз в 60 секунд')
        return
    else:
        await call.message.answer('Баланс успешно пополнен')
        await update_user_balance(call.from_user.id, payment.rub)
        await call.message.delete_reply_markup()
        user = await select_user(call.from_user.id)
        if user.referral != 0:
            user_referral = await select_user(user.referral)
            percent = await get_bot_settings()
            percent = percent.referral_percent
            if user_referral.referral_percent is not None:
                percent = user_referral.referral_percent
            balance_add = math.floor(payment.rub // 100 * percent)
            await update_user_balance(user.referral, balance_add)
            try:
                await bot.send_message(user_id=user.referral, text=f'Отчисление за реферала: {balance_add}')
            except:
                pass
    await state.finish()


@dp.callback_query_handler(text_contains='btc')
async def payment_balance_btc_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    sett = await get_bot_settings()
    await call.message.answer(sett.text_btc, reply_markup=close())

price = Price()
@dp.message_handler(state='write_balance_btc')
async def payment_handler_btc_two(message: Message, state: FSMContext):
    if message.text != '💰Отмена':
        settings = await get_bot_settings()
        amount = price.rub_sat(int(message.text)) + randint(5, 200)
        payment = Payment(amount=amount, rub=int(message.text))
        payment.create()

        await message.answer('Меню', reply_markup=menu_start())
        show_amount = blockcypher.from_satoshis(payment.amount, 'btc')
        await message.answer(f'Оплатите {show_amount:.8f} на биткоин адрес <pre>{settings.address_btc}</pre>\n\n💡Переводить строго указанную сумму, иначе платеж не будет зачислен\n\n😡Для отмены обработки оплаты нажмите на кнопку ниже', parse_mode='HTML',
                             reply_markup=return_check_payment())
        await state.set_state('check_btc')
        await state.update_data(payment=payment)
    else:
        await message.answer('Вы успешно отменили оплату', reply_markup=menu_start())
        await state.finish()


@dp.callback_query_handler(text_contains='close_message', state='check_btc')
async def close_message_handler(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('Оплата успешно отменена')
    await state.finish()


@dp.message_handler(text='📥Помощь')
async def help_text_handler(message: Message):
    settings = await get_bot_settings()
    if settings.help_text == '':
        await message.answer('Текст не заполнен администратором')
        return
    await message.answer(settings.help_text)



@dp.message_handler(IsAdmin(), commands=['add', 'zam'])
async def add_money(message: Message):
    data = message.text.split(" ")
    if len(data)!=3:
        return await message.answer("Использование команды: /add(zam) {user_id} {сумма}")
    u = User.objects.filter(user_id=data[1]).first()
    if u==None:
        return await message.answer(f"Пользователь с ID {data[1]} не найден!")
    money = data[2]
    if not money.isdigit():
        return await message.answer(f"Сумма {money} не является числовым значением!")
    money=int(money)
    u.balance+=money
    u.save()
    try:
        if data[0]=="/add":
            text = f"Ваш баланс пополнен на {money} рублей!"
        elif data[0]=="/zam":
            text = f"Баланс профиля пополнен по замене на {money} рублей!"
        await bot.send_message(u.user_id, text)
        await message.answer(f"Баланс пользователя с ID {data[1]} успешно пополнен на {money} рублей!")
    except Exception as ex:
        await message.answer(f"Кажется, пользователь заблокировал бота, баланс был пополнен!\n{repr(ex)}")

@dp.callback_query_handler(lambda x: x.data.startswith("zam") or x.data.startswith("add"))
async def change_call_handler(call: CallbackQuery):
    # settings = await get_bot_settings()
    # if settings.admin_id!=message.from_user.id:
    #     return
    data = call.data.split(" ")
    if len(data)!=3:
        return await call.answer("Использование команды: /add(zam) {user_id} {сумма}", True)
    u = User.objects.filter(user_id=data[1]).first()
    if u==None:
        return await call.answer(f"Пользователь с ID {data[1]} не найден!", True)
    money = data[2]
    if not money.isdigit():
        return await call.answer(f"Сумма {money} не является циферным значением!", True)
    money=int(money)
    u.balance+=money
    u.save()
    Payment.objects.create(from_user=u, amount=money)
    try:
        text = f"Баланс профиля пополнен по замене на {money} рублей!"
        if data[0]=="add":
            text = f"Заявка одобрена, баланс пополнен на {money} рублей!"
            if u.referral != 0:
                user_referral = await select_user(u.referral)
                percent = await get_bot_settings()
                percent = percent.referral_percent
                if user_referral.referral_percent is not None:
                    percent = user_referral.referral_percent
                balance_add = math.floor(money//100*percent)
                await update_user_balance(u.referral, balance_add)
                try:
                    await bot.send_message(user_id=u.referral, text=f'Отчисление за реферала: {balance_add}')
                except:
                    pass
            
        await bot.send_message(u.user_id, text)
        await call.answer(f"Баланс пользователя с ID {data[1]} успешно пополнен на {money} рублей!", True)
        await call.message.delete()
    except Exception as ex:
        await call.answer(f"Кажется, пользователь заблокировал бота, баланс был пополнен!\n{repr(ex)}", True)

def get_admins():
    settings = BotSettings.objects.first()
    return settings.admin_id.split("\r\n")


async def get_qiwi():
    qiwi = Qiwi.objects.filter(active=True).first()
    if qiwi==None:
        try:
            await bot.send_message(get_admins()[0], "Аккаунты закончились, оплаты приостановлены.\nПожалуйста, добавьте аккаунты в админке.")
        except:
            pass
        return False
    wallet = FuckingCard(qiwi.token, qiwi.info, qiwi.card_num)
    return wallet


@dp.message_handler(IsAdmin(), commands=['stat',])
async def stat_handler(message: Message):
    await message.delete()
    week = datetime.datetime.now() - datetime.timedelta(days=7)
    allbuys = AllBuyProduct.objects.order_by('-date')
    stat = {}
    day_stat = {}
    week_text = ""
    for bough in allbuys.filter(date__gte=week):
        if "trafger" in bough.user.username.lower():
            continue
        date = f"{djdate(bough.date, 'd.m')}"
        if not date in day_stat:
            day_stat[date] = bough.sum
        else:
            day_stat[date] += bough.sum
    for day in day_stat:
        week_text+=f" - {day}: <code>{day_stat[day]}₽</code>\n"
    for bough in allbuys:
        if "trafger" in bough.user.username.lower():
            continue
        date = f"{djdate(bough.date, 'F, Y')}"
        if not date in stat:
            stat[date] = bough.sum
        else:
            stat[date] += bough.sum
    stat_text = "<b>Статистика покупок:</b>\n\n"
    i=0
    for month in stat:
        if i==0:
            stat_text += f"{month}: <code>{stat[month]}₽</code>\n{week_text}\n"
        else:
            stat_text+=f"{month}: <code>{stat[month]}₽</code>\n\n"
        i+=1
    await message.answer(stat_text, reply_markup=close())
