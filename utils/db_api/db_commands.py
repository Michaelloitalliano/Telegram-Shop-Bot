from django.db.models import Sum

from django_project.telegrambot.usersmanage.models import *
from asgiref.sync import sync_to_async

from datetime import datetime

@sync_to_async
def add_user(user_id, username):
    try:
        return User.objects.get(user_id=user_id)
    except Exception:
        return User.objects.create(user_id=user_id, username=username)


@sync_to_async
def get_shop_help_text():
    return BotSettings.objects.first().help_text_shop


@sync_to_async
def get_start_text():
    return BotSettings.objects.first().start_text


@sync_to_async
def select_user(user_id=None, username=None):
    if username is not None:
        return User.objects.filter(username=username).first()
    user = User.objects.filter(user_id=user_id).first()
    return user


@sync_to_async
def minus_user_money(user_id, balance):
    user = User.objects.get(user_id=user_id)
    user.balance = user.balance - int(balance)
    user.save()


@sync_to_async
def add_referral(user_id, referral):
    user = User.objects.get(user_id=user_id)
    user.referral = referral
    user.save()
    user = User.objects.get(user_id=referral)


@sync_to_async
def all_product():
    product = Product.objects.all()
    return product


@sync_to_async
def get_subcategory(pk=None, category=None):
    subcategory = SubCategory.objects.get(pk=pk)
    return subcategory


@sync_to_async
def get_category(pk):
    category = Category.objects.get(pk=pk)
    return category


@sync_to_async
def get_subcategory_product(pk):
    product = Product.objects.filter(subcategory_id=pk)
    return product


@sync_to_async
def get_product(pk):
    return Product.objects.filter(pk=pk)


@sync_to_async
def get_product_for_get(pk):
    return Product.objects.get(pk=pk)


@sync_to_async
def update_product_string(pk, product_update):
    a = Product.objects.get(pk=pk)
    a.product_this = product_update
    a.save()


@sync_to_async
def get_bot_settings():
    return BotSettings.objects.first()


@sync_to_async
def get_all_user_referral(user_id):
    return User.objects.filter(referral=user_id).count()


@sync_to_async
def update_user_balance(user_id, balance):
    u = User.objects.get(user_id=user_id)
    u.balance = u.balance + balance
    u.save()


@sync_to_async
def update_count_buy(user_id):
    u = User.objects.get(user_id=user_id)
    u.count_buy = u.count_buy + 1
    u.save()


@sync_to_async
def update_username(user_id, username):
    u = User.objects.get(user_id=user_id)
    u.username = username
    u.save()


@sync_to_async
def get_all_subcategory(pk):
    return SubCategory.objects.filter(category__id=pk)


@sync_to_async
def get_product_subcategory(pk):
    return Product.objects.filter(subcategory__pk=pk)


@sync_to_async
def get_all_user():
    return User.objects.all()


@sync_to_async
def get_all_product():
    return Product.objects.all()


@sync_to_async
def create_buy_product(user, product, count, sum):
    AllBuyProduct.objects.create(
        user=user,
        product=product,
        count=count,
        sum=sum,
        date=datetime.now()
    )
