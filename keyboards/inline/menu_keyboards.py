from .CallBack_Data import open_callback, buy_product_callback, buy_product_this_callback

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.db_commands import all_product, get_subcategory, get_category, \
    get_subcategory_product, get_product_subcategory, get_all_subcategory
from utils.create_text_message import count_product
from django_project.telegrambot.usersmanage.models import PaySystem


def change(user_id, amount):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='✅ Заменить ✅', callback_data=f'zam {user_id} {amount}'))
    return markup

def fuck(user_id, amount):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='✅ Пополнить ✅', callback_data=f'add {user_id} {amount}'))
    markup.add(InlineKeyboardButton(text='🖕 Плохой человек 🖕', callback_data=f'fuck {user_id} {amount}'))
    return markup

def return_back_btn():
    return InlineKeyboardButton(text='❌Закрыть❌', callback_data='close_message')

def close():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='❌Закрыть❌', callback_data='close_message'))
    return markup

def agreement():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='✅ Принять', callback_data='agree'),InlineKeyboardButton(text='❌ Отказаться', callback_data='close_message'))
    return markup

async def return_category():
    markup = InlineKeyboardMarkup()
    have = []
    Product = await all_product()
    for product in Product:
        if count_product(product.product_this) > 0:
            subcategory = await get_subcategory(product.subcategory_id)
            category = await get_category(subcategory.category_id)
            if category.pk not in have:
                markup.add(InlineKeyboardButton(text=category.name,
                                                callback_data=open_callback.new(id=category.pk, name='subcategory_open')))
                have.append(category.pk)
    markup.add(return_back_btn())
    return markup


async def return_subcategory(pk):
    category_uid = pk
    markup = InlineKeyboardMarkup()
    have = []
    subcategory = await get_all_subcategory(category_uid)
    for subcat in subcategory:
        Product_sub = await get_product_subcategory(subcat.pk)
        for product in Product_sub:
            if count_product(product.product_this) > 0:
                if subcat.pk not in have:
                    markup.add(InlineKeyboardButton(text=f"{subcat.name}",
                                                    callback_data=open_callback.new(name='product_open_is_subcategory',
                                                                                    id=subcat.pk)))
                    have.append(subcat.pk)
                    break
    markup.add(return_back_btn())
    return markup


async def return_product(pk):
    markup = InlineKeyboardMarkup()
    have = []
    Product = await get_subcategory_product(pk)
    for product in Product:
        if count_product(product.product_this) > 0:
            if product.pk not in have:
                markup.add(InlineKeyboardButton(text=f'♻ {product.name} | {product.cost} руб',
                                                callback_data=open_callback.new(name='product_open',
                                                                                id=product.pk)))
                have.append(product.pk)
    markup.add(return_back_btn())
    return markup


def return_buy_product(pk):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Купить', callback_data=open_callback.new(name='buy_product', id=pk)))
    return markup


def confirm_buy_product(count, cost, pk):
    markup = InlineKeyboardMarkup()
    if count == 'no':
        markup.add(InlineKeyboardButton(text='Подтвердить', callback_data=buy_product_callback.new(cost=cost,
                                                                                                   pk=pk, count=count)))
    else:
        markup.add(InlineKeyboardButton(text='Подтвердить', callback_data=buy_product_this_callback.new(cost=cost,
                                                                                                   pk=pk, count=count, name='conf')))
    return markup


# def return_chose_payment():
#     markup = InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton(text='Биткоин', callback_data='btc'))
#     markup.add(InlineKeyboardButton(text='Киви', callback_data='qiwi'))
#     return markup
def return_chose_payment():
    markup = InlineKeyboardMarkup()
    for system in PaySystem.objects.filter(active=True):
        markup.add(InlineKeyboardButton(text=system.name, callback_data=f'pay {system.id}'))
    # markup.add(InlineKeyboardButton(text='Биткоин', callback_data='btc'))
    markup.add(InlineKeyboardButton(text='Киви', callback_data='qiwi'))
    markup.add(InlineKeyboardButton(text='Visa/MasterCard RU', callback_data='zver'))
    markup.add(InlineKeyboardButton(text='Visa/MasterCard UA', callback_data='zver_UA'))
    return markup


def return_check_payment():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Проверить оплату', callback_data='check_payment_btc'))
    markup.add(InlineKeyboardButton(text='ОТМЕНИТЬ ОПЛАТУ', callback_data='close_message'))
    return markup
