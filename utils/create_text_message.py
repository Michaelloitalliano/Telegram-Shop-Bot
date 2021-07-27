def create_info_product(name, cost, description, count):
    if description == '':
        text = f'''
🚀Название товара: {name}
💰Стоимость товара: {cost} руб
💡Количество товара: {count}

✅Для начала оформления процесса покупки нажмите на кнопку ниже'''
    else:
        text = f"""
🚀Название товара: {name}
💰Стоимость товара: {cost} руб
💡Количество товара: {count}
😳Описание товара: {description}

✅Для начала оформления процесса покупки нажмите на кнопку ниже
"""
    return text


def count_product(product):
    if not product:
        return 0

    count = product.count('\n')
    if not product.endswith('\n'):
        count += 1
    return count


def buy_product_text(count, name, cost):
    text = f"""
Вы уверены что хотите преобрести данный товар❓

💶Название товара: {name}
💡Регионы: {count}
🎁Стоимость товара: {cost} руб

✅Для подтверждения покупки нажмите на кнопку ниже✅"""
    return text

def buy_product_text_cvv(count, name, cost):
    text = f"""
Вы уверены что хотите преобрести данный товар❓

💶Название товара: {name}
💡Количество: {count}
🎁Стоимость товара: {cost} руб

✅Для подтверждения покупки нажмите на кнопку ниже✅"""
    return text


def return_referral_text(percent, link, count_ref):
    text = f"""
👤Ваш реферер: 
Процент возврата по реферальной программе {percent}%
Ваша реферальная ссылка: {link}
Количество ваших рефералов: {count_ref}
"""
    return text


def return_profile_text(user_id, username, balance, count_buy):
    text = f"""
Ваш профиль:
🕶️ Ваш ID: {user_id}
👏 Ваш никнейм: @{username}
🏦 Ваш текущий баланс: {balance} руб.
💥 Покупок:  {count_buy}
"""
    return text


# def return_payment_text(count):
#     return f'''
# ✅Оплата через систему Qiwi✅
# 💡Для оплаты перейдите по ссылке в кнопке
# ⏰Счет действителен в течение часа
# 💰Сумма к оплате: {count} руб

# ❗️После оплаты нажмите на кнопку ниже
# '''
def return_payment_text(qiwi_p2p, amount):
    return f"Переводить строго сумму: {amount}"

def return_zver_payment_text(amount):
    return f"💰Сумма к оплате: {amount} руб"