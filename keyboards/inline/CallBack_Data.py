from aiogram.utils.callback_data import CallbackData

open_callback = CallbackData('subcategory', 'name', 'id')

buy_product_callback = CallbackData('product_buy', 'cost', 'count', 'pk')

buy_product_this_callback = CallbackData('product_buy_this_count', 'cost', 'count', 'pk', 'name')

create_payment_callback = CallbackData('payment_callback', 'name', 'bill_id')

user_garant_list = CallbackData('list_user_info', 'name', 'pk')

user_create_trade = CallbackData('create_trade', 'sum', 'user_id')