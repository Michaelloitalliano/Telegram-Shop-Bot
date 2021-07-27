from aiogram.types import ReplyKeyboardMarkup


def shop_reset_buy():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('💢Отменить')
    return markup