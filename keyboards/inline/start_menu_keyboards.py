from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .CallBack_Data import create_payment_callback


def create_payment_button(bill_id, url):
    markup = InlineKeyboardMarkup()
    btn_url = InlineKeyboardButton(text='🚀Ссылка на оплату', url=url)
    btn_check = InlineKeyboardButton(text='😎Я оплатил',
                                     callback_data=create_payment_callback.new(name='check_pay',
                                                                               bill_id=bill_id))
    markup.add(btn_url)
    markup.add(btn_check)
    markup.add(InlineKeyboardButton(text='❌Закрыть❌', callback_data='close_message'))
    return markup
