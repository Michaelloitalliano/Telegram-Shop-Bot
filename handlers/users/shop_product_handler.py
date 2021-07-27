import os, zipfile

from loader import dp, bot

import logging, shutil, re

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup
from aiogram import types

from keyboards.inline import return_category, return_subcategory, return_product, return_buy_product, \
    confirm_buy_product
from keyboards.default import menu_start, shop_reset_buy, reset_payment_keyboard
from keyboards.inline.CallBack_Data import open_callback, buy_product_callback, buy_product_this_callback
from keyboards.inline.menu_keyboards import return_back_btn, agreement, close, change

from utils.db_api.db_commands import get_product, select_user, minus_user_money, update_product_string, \
    get_shop_help_text, update_count_buy, create_buy_product, get_bot_settings
from utils.create_text_message import create_info_product, count_product, buy_product_text, buy_product_text_cvv
from django_project.telegrambot.usersmanage.models import *
from filters.is_admin import IsAdmin


@dp.message_handler(state='write_log')
async def log_name_handler(message: Message, state: FSMContext):
    log_name_src = message.text
    if log_name_src=='💰Отмена':
        await state.finish()
        return await message.answer('Действие отменено', reply_markup=menu_start())
    user = await select_user(message.from_user.id)
    need_logs = []
    work_dir = "change_log"
    if not os.path.isdir(work_dir):
        os.mkdir(work_dir)
    all_names = log_name_src.split("\n")
    if len(all_names)>25:
        return await message.answer("В одной заявке можно указать не более 25 файлов одного товара.\nПопробуйте ещё раз или нажмите кнопку отмены.")
    worked = []
    for log_name in all_names:
        if log_name in worked:
            return await message.answer(f"Повторно указан {log_name}\nПопробуйте ещё раз или нажмите кнопку отмены.", reply_markup=reset_payment_keyboard())
        log_name = log_name.replace(" ", "")
        log = LogFileID.objects.filter(user=user, log_name=log_name).first()
        if log==None:
            return await message.answer(f"Файл {log_name} не найден!\nПопробуйте ещё раз или нажмите кнопку отмены.", reply_markup=reset_payment_keyboard())
        if log.worked:
            return await message.answer(f"Файл {log_name} уже был заменен, либо была отправлена заявка!\nПопробуйте ещё раз или нажмите кнопку отмены.", reply_markup=reset_payment_keyboard())
        delim = (datetime.datetime.now(tz=None)-datetime.timedelta(hours=3))-log.date.replace(tzinfo=None)
        if delim.days!=0:
            return await message.answer(f"🕓 На замену дается 24 часа с момента покупки. Часовой период для замены {log_name} прошёл.\nПопробуйте ещё раз или нажмите кнопку отмены.", reply_markup=reset_payment_keyboard())
        need_logs.append(log)
        worked.append(log_name)
    result_name = f'{work_dir}{os.sep}{user.user_id}_{len(all_names)}шт.zip'
    logzip = zipfile.ZipFile(result_name, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9)
    for need_log in need_logs:
        if not os.path.isdir(os.path.join(work_dir, need_log.log_name)):
            zipname = os.path.join(work_dir, "tmp.zip")
            await bot.download_file_by_id(need_log.file_id, zipname)
            zip = zipfile.ZipFile(zipname)
            zip.extractall(work_dir)
            zip.close
        for root, dirs, files in os.walk(os.path.join(work_dir, need_log.log_name)):
            for file in files:
                logzip.write(os.path.join(root,file), arcname=os.sep.join(os.path.join(root,file).split(os.sep)[1:]))
        need_log.worked=True
        need_log.save()
    logzip.close()
    try:
        ch_id = "CHANNEL_ID"
        text = f"Пользователь: {user.username} #u{user.user_id}\n"\
            f"Название товара: {log.product}\n"
        product = Product.objects.filter(name=log.product).first()
        amount = product.cost*len(all_names)
        await bot.send_document(ch_id, open(result_name, "rb"), caption=text, reply_markup=change(user.user_id, amount))
        await state.finish()
        await message.answer("Запрос на замену отправлен, ожидайте.", reply_markup=menu_start())
        shutil.rmtree(work_dir)
    except Exception as ex:
        logging.info(f"{repr(ex)}")
        await state.finish()
        return await message.answer('Произошла ошибка. Попробуйте позже или обратитесь к продавцу.', reply_markup=menu_start())

@dp.message_handler(text='📖Правила')
async def rules_handler(message: Message):
    return await message.answer(agreement_text, reply_markup=close())

@dp.message_handler(text='😎Наличие товаров')
async def shop_all_category(message: Message):
    user = await select_user(message.from_user.id)
    if not user.agreement:
        return await message.answer(agreement_text, reply_markup=agreement())
    markup = await return_category()
    if str(markup) == '{"inline_keyboard": [[{"text": "❌Закрыть❌", "callback_data": "close_message"}]]}':
        await message.answer('😞На данный момент нет доступных товаров, заходи позже')
    else:
        text_info = 'Информация по остаткам\n\n'
        for product in Product.objects.all():
            if product.subcategory.text_mode:
                text_info+=f"{product.name} | {len(product.product_this.splitlines())} шт.\n"
            else:
                text_info+=f"{product.name} | {len(LogLink.objects.filter(product=product))} шт.\n"
        await message.answer(f'{text_info}\n\n😎Выберите интересующую вас категорию', reply_markup=markup)


@dp.message_handler(text='❌Главное меню')
async def exit_start_menu(message: Message):
    await message.answer('🚀Вы успешно вернулись в стартовое меню', reply_markup=menu_start())


@dp.callback_query_handler(open_callback.filter(name='subcategory_open'))
async def show_all_subcategory(call: CallbackQuery, callback_data: dict):
    pk = callback_data.get('id')
    markup = await return_subcategory(pk)
    if str(markup) == '{"inline_keyboard": [[{"text": "❌Закрыть❌", "callback_data": "close_message"}]]}':
        await call.message.edit_text('😞На данный момент нет доступных товаров, заходи позже',
                                     reply_markup=InlineKeyboardMarkup())
    else:
        await call.message.edit_text('😎Выберите интересующую вас подкатегорию', reply_markup=markup)


@dp.callback_query_handler(open_callback.filter(name='product_open_is_subcategory'))
async def show_all_product(call: CallbackQuery, callback_data: dict):
    subcategory_id = callback_data.get('id')
    markup = await return_product(subcategory_id)
    if str(markup) == '{"inline_keyboard": [[{"text": "❌Закрыть❌", "callback_data": "close_message"}]]}':
        await call.message.edit_text('😞На данный момент нет доступных товаров, заходи позже',
                                     reply_markup=InlineKeyboardMarkup())
    else:
        await call.message.edit_text('😎Выберите интересующий вас товар', reply_markup=markup)


@dp.callback_query_handler(text_contains='close_message')
async def close_message(call: CallbackQuery):
    await call.message.delete()


@dp.message_handler(text='📥Помощь')
async def shop_help_text_handler(message: Message):
    text = await get_shop_help_text()
    if text == '':
        return await message.answer('Текст не задан администратором')
    await message.answer(text)


@dp.callback_query_handler(open_callback.filter(name='product_open'))
async def show_product(call: CallbackQuery, callback_data: dict):
    product_id = callback_data.get('id')
    product = await get_product(product_id)
    if product.first() is None:
        await call.message.edit_text('😢Товар не найден, возможно он был удален')
    else:
        product = product.first()
        if product.subcategory.text_mode:
            count = len(product.product_this.splitlines())
        else:
            if product.no_limit:
                count = 'Безлимитный товар'
            else:
                count = len(LogLink.objects.filter(product=product))
        if count == 0:
            return await call.message.edit_text('😞Этот товар уже закончился')
        await call.message.edit_text(create_info_product(product.name, product.cost, product.description, count),
                                     reply_markup=return_buy_product(product_id))


@dp.callback_query_handler(open_callback.filter(name='buy_product'))
async def buy_product_step_first(call: CallbackQuery, callback_data: dict, state: FSMContext):
    id = callback_data.get('id')
    product = await get_product(id)
    if product.first().no_limit:
        return await call.message.edit_text(buy_product_text(1, product.first().name, product.first().cost),
                                            reply_markup=confirm_buy_product('no',
                                                                             product.first().cost,
                                                                             product.first().pk))
    
    if product.first().subcategory.text_mode:
        logs = product.first().product_this.splitlines()
    else:
        logs = LogLink.objects.filter(product=product.first())
    if len(logs) == 0:
        return await call.message.edit_text('😞Этот товар уже закончился')
    else:
        await call.message.delete()
        await state.set_state('write_count')
        await state.update_data({'product_id': id})

        if product.first().subcategory.text_mode:
            count = len(logs)
            return await call.message.answer(f'<b>Наличие {product.first().name}: {count}шт.</b>\n\nВведите необходимое количество товара.', reply_markup=shop_reset_buy())

        regions = {}
        for log in logs:
            if log.reg in regions:
                regions[log.reg]+=1
            else:
                regions[log.reg]=1
        msg_reg = []
        if not product.first().subcategory.only_all:
            for region in regions:
                msg_reg.append(f"{region} - {regions[region]} шт.")
        msg_reg.sort()
        msg_reg.append(f"ALL - {len(logs)} шт.")
        await call.message.answer(
            text=f'<b>Наличие {product.first().name}:</b>\n{" | ".join(msg_reg)}\n\n<b>Введите регион интересующих afqkjd и их количество.</b>\n<code>Пример: TK 5,GB 2\n❗️ Указывать можно <b>не больше пяти</b> регионов за одну покупку.</code>',
            reply_markup=shop_reset_buy(), parse_mode="html")


@dp.message_handler(text=['💢Отменить', '💰Отмена'], state='*')
async def delete_state_handler_now(message: Message, state: FSMContext):
    await message.answer('Вы успешно отменили активный state', reply_markup=menu_start())
    await state.finish()


@dp.message_handler(state='write_count')
async def count_buy(message: Message, state: FSMContext):
    if not message.text:
        return await message.answer('❌Количество товара должно быть в формате <code>TK 5, GB 2</code>\n✅Попробуйте еще раз или нажмите на кнопку "отмены"', parse_mode="html")
    data = await state.get_data()
    id = data.get('product_id')
    product = await get_product(id)

    if product.first().subcategory.text_mode:
        count = len(product.first().product_this.splitlines())
        need_count = message.text
        if not need_count.isdigit():
            return await message.answer(f'❌Количество товара должно быть числом от 1 до {count}\n✅Попробуйте еще раз или нажмите на кнопку "отмены"', parse_mode="html")
        need_count = int(need_count)
        if need_count>count:
            return await message.answer(f'❌Количество товара должно быть числом от 1 до {count}\n✅Попробуйте еще раз или нажмите на кнопку "отмены"', parse_mode="html")
        await state.finish()
        await message.answer(buy_product_text_cvv(message.text, product.first().name, product.first().cost * need_count), reply_markup=confirm_buy_product(message.text, product.first().cost * need_count, product.first().pk))
        return await message.answer('Выход в меню..', reply_markup=menu_start())

    products_need = message.text.split(",")
    allcount=0
    rgs = []
    for product_need in products_need:
        params = product_need.split(" ")
        if len(params)!=2:
            return await message.answer('❌Количество товара должно быть в формате <code>TK 5, GB 2</code>. Наличие указано выше.\n✅Попробуйте еще раз или нажмите на кнопку "отмены"', parse_mode="html")
        reg, count = params
        if reg in rgs:
            return await message.answer('❌Один регион не может быть указан дважды.\n✅Попробуйте еще раз или нажмите на кнопку "отмены"', parse_mode="html")
        rgs.append(reg)
        if not str(count).isdigit():
            return await message.answer('❌Количество товара должно быть в формате <code>TK 5, GB 2</code>. Наличие указано выше.\n✅Попробуйте еще раз или нажмите на кнопку "отмены"', parse_mode="html")
        if reg=='ALL':
            if (len(LogLink.objects.filter(product=product.first()))-allcount)<int(count):
                return await message.answer(f'Ошибка в \"{product_need}\"\n❌Количество товара должно быть в формате <code>TK 5, GB 2</code>. Наличие указано выше.\n✅Попробуйте еще раз или нажмите на кнопку "отмены"', parse_mode="html")
            allcount+=int(count)
            continue
        if len(LogLink.objects.filter(product=product.first(), reg=reg))<int(count):
            return await message.answer(f'Ошибка в \"{product_need}\"\n❌Количество товара должно быть в формате <code>TK 5, GB 2</code>. Наличие указано выше.\n✅Попробуйте еще раз или нажмите на кнопку "отмены"', parse_mode="html")
        allcount+=int(count)
    try:
        await message.answer(buy_product_text(message.text, product.first().name, product.first().cost * allcount),
                         reply_markup=confirm_buy_product(message.text, product.first().cost * allcount, product.first().pk))
        await message.answer('Выход в меню..', reply_markup=menu_start())
    except ValueError:
        return await message.answer("❗️ Указывать можно <b>не больше пяти</b> регионов за одну покупку.\n✅Попробуйте еще раз или нажмите на кнопку \"отмены\"")
    await state.finish()


@dp.callback_query_handler(buy_product_this_callback.filter(name='conf'))
async def buy_product_has_count(call: CallbackQuery, callback_data: dict):
    cost = callback_data.get('cost')
    user = await select_user(call.from_user.id)
    if user.balance<int(cost):
        return await call.message.answer('Недостаточно средств')
    await call.message.delete()
    product_id = callback_data.get('pk')
    product = await get_product(product_id)
    
    prd = product.first()
    if prd.subcategory.text_mode:
        count = int(callback_data.get("count"))
        cvvs = prd.product_this.splitlines()
        need = cvvs[:count]
        for card in need:
            CvvHistory.objects.create(card=f"{prd.subcategory.name}:{prd.name}:{card}")
        prd.product_this = "\n".join(cvvs[count:])
        prd.save()
        fname = f'generate_file/{call.from_user.id}:{product_id}.txt'
        with open(fname, 'w') as file:
            file.write("\n".join(need))
        await call.message.answer_document(open(fname, "rb"), caption="Спасибо за покупку!")
        await minus_user_money(call.from_user.id, cost)
        logging.info(f'Пользователь {call.from_user.username} купил {prd.name}: {count}')
        await create_buy_product(user, prd.name, count, cost)
        return await update_count_buy(call.from_user.id)
    
    dirs_need = []
    for product_need in callback_data.get('count').split(","):
        reg, log_count = product_need.split(" ")
        for _ in range(int(log_count)):
            if reg == 'ALL':
                log = LogLink.objects.filter(product=product.first()).first()
            else:
                log = LogLink.objects.filter(product=product.first(), reg=reg).first()
            log.delete()
            dirs_need.append(log.link)
    all_count = len(dirs_need)
    need_ids = []
    max_logs = 50
    if all_count>max_logs:
        for dec in range(int(all_count/max_logs)):
            zipname = f'{call.from_user.id}_part{dec}.zip'
            logzip = zipfile.ZipFile(zipname, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9)
            i=0
            for num in range(all_count):
                if len(dirs_need)<=0:
                    break
                dirc = dirs_need[-1]
                if not os.path.isdir(dirc):
                    logging.info(f'wtf!? {dirc}')
                    continue
                if i==max_logs:
                    break
                for root, dirs, files in os.walk(dirc):
                    for file in files:
                        logzip.write(os.path.join(root,file), arcname=os.path.join(root,file).replace(f"logs{os.sep}{product_id}{os.sep}",""))
                if not product.first().no_change:
                    log_file = LogFileID.objects.create(user=user, product=product.first().name, log_name=dirc.split(os.sep)[2])
                    need_ids.append(log_file)
                dirs_need.remove(dirc)
                shutil.rmtree(dirc)
                i+=1
            logzip.close()
            try:
                ans = await call.message.answer_document(document=open(zipname, 'rb'), caption=f'Спасибо за покупку!')
                for logid in need_ids:
                    logid.file_id = ans.document.file_id
                    logid.save()
                need_ids.clear()
                os.remove(zipname)
            except Exception as ex:
                logging.info(f'ERROR: {ex}')
        #start
        if len(dirs_need)>0:
            logzip = zipfile.ZipFile(f'{call.from_user.id}_end.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9)
            for dirc in dirs_need:
                if not os.path.isdir(dirc):
                    continue
                for root, dirs, files in os.walk(dirc):
                    for file in files:
                        logzip.write(os.path.join(root,file), arcname=os.path.join(root,file).replace(f"logs{os.sep}{product_id}{os.sep}",""))
                if not product.first().no_change:
                    log_file = LogFileID.objects.create(user=user, product=product.first().name, log_name=dirc.split(os.sep)[2])
                    need_ids.append(log_file)
                shutil.rmtree(dirc)
            logzip.close()
            try:
                ans = await call.message.answer_document(document=open(f'{call.from_user.id}_end.zip', 'rb'), caption=f'Спасибо за покупку!')
                for logid in need_ids:
                    logid.file_id = ans.document.file_id
                    logid.save()
                need_ids.clear()
                os.remove(f'{call.from_user.id}_end.zip')
            except Exception as ex:
                print(f'ERROR: {ex}')
    elif all_count<=max_logs:
        logzip = zipfile.ZipFile(f'{call.from_user.id}.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9)
        for dirc in dirs_need:
            if not os.path.isdir(dirc):
                continue
            logging.info(f"{dirc.split(os.sep)[2]}")
            for root, dirs, files in os.walk(dirc):
                for file in files:
                    logzip.write(os.path.join(root,file), arcname=os.path.join(root,file).replace(f"logs{os.sep}{product_id}{os.sep}",""))
            if not product.first().no_change:
                log_file = LogFileID.objects.create(user=user, product=product.first().name, log_name=dirc.split(os.sep)[2])
                need_ids.append(log_file)
            shutil.rmtree(dirc)
        logzip.close()
        try:
            ans = await call.message.answer_document(document=open(f'{call.from_user.id}.zip', 'rb'), caption=f'Спасибо за покупку!')
            for logid in need_ids:
                logid.file_id = ans.document.file_id
                logid.save()
            need_ids.clear()
            os.remove(f'{call.from_user.id}.zip')
        except Exception as ex:
            print(f'ERROR: {ex}')
    await minus_user_money(call.from_user.id, cost)
    logging.info(f'Пользователь {call.from_user.username} купил {product.first().name}: {callback_data.get("count")}')
    await create_buy_product(user, product.first().name, all_count, cost)
    await update_count_buy(call.from_user.id)


@dp.message_handler(IsAdmin(), commands=['rem'])
async def bot_start(message: types.Message):
    from_id = message.from_user.id
    data = message.text.split(" ")
    settings = await get_bot_settings()
    if len(data)!=2:
        await message.answer("Ожидался ID товара", reply_markup=return_back_btn())
        return
    product_id = data[1]
    if not Product.objects.filter(id=product_id).exists():
        await message.answer("ID Товара не найден", reply_markup=return_back_btn())
        return
    product = Product.objects.get(id=product_id)
    logs = LogLink.objects.filter(product=product)
    i=0
    for log in logs:
        shutil.rmtree(log.link)
        log.delete()
        i+=1
    await message.answer(f"Успешно удалено {i} логов товара {product}")


agreement_text = """Правила"""


@dp.message_handler(IsAdmin(), commands=['find'])
async def pizdec(message: types.Message):
    from_id = message.from_user.id
    data = message.text.split(" ")
    logs = LogLink.objects.all()
    products = Product.objects.all()
    ids = [74,75,76,77,78,79,80,81,84]
    alllogfiles = []
    info = {}
    for product in products:
        id = product.id
        files = os.listdir(f"logs/{id}/")
        info[id] = 0
        for file in files:
            loglink = f"logs/{id}/{file}"
            if logs.filter(link=loglink).count()==0:
                info[id] += 1
                alllogfiles.append(loglink)
                # if not os.path.isdir(f"lost/{id}"):
                #     os.mkdir(f"lost/{id}")
                # shutil.copytree(loglink, f"lost/{id}/{file}")
                # shutil.rmtree(loglink)
    text = ""
    if len(alllogfiles)!=0:
        for id in info:
            text += f"{id} - {info[id]}\n"
        with open("all.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(alllogfiles))
        await message.answer_document(open("all.txt", encoding="utf-8"), caption=text)
    else:
        await message.answer("Расхождений не найдено", reply_markup=close())