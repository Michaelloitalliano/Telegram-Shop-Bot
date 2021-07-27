from django.db import models
from django.utils import timezone
import datetime


class User(models.Model):
    user_id = models.PositiveIntegerField(verbose_name='Telegram Id', null=False)
    username = models.TextField(verbose_name='Telegram username', null=False)
    balance = models.IntegerField(verbose_name='Баланс', default=0)
    count_buy = models.PositiveIntegerField(verbose_name='Кол-во покупок', default=0)
    referral = models.PositiveIntegerField(verbose_name='Реферал', default=0, blank=True)
    referral_percent = models.PositiveIntegerField(verbose_name='Персональный реф %', null=True, blank=True)
    agreement = models.BooleanField(verbose_name='Правила', default=False)

    objects = models.Manager()

    def __str__(self):
        if self.username != '@None':
            return f'{self.username}'
        else:
            return f'{self.user_id}'

    class Meta:
        verbose_name = '1. Пользователь'
        verbose_name_plural = '1. Пользователи'


class Category(models.Model):
    name = models.TextField(verbose_name='Название категории', max_length=35, null=False)

    objects = models.Manager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = '3. Категория'


class SubCategory(models.Model):
    name = models.TextField(verbose_name='Название подкатегории', max_length=35, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text='Выберите категорию',
                                 verbose_name='Категория')
    text_mode = models.BooleanField(verbose_name='Режим строк', default=False)
    parse_type = models.IntegerField(verbose_name='Режим парсинга', choices=[(1, "Старый тип"), (2, "Новый тип")], default=1)
    only_all = models.BooleanField(verbose_name="Только ALL в регионах", default=False)

    objects = models.Manager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'подкатегорию'
        verbose_name_plural = '4. Подкатегория'

class Product(models.Model):
    name = models.TextField(verbose_name='Название товара', max_length=35, null=False)
    product_this = models.TextField(verbose_name='Товар', max_length=100000, null=False,
                                    help_text='Один товар - одна строчка')
    cost = models.PositiveIntegerField(verbose_name='Стоимость товара', null=False)
    description = models.TextField(verbose_name='Описание товара', null=True, blank=True,
                                   help_text='Сюда писать описание товара')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, help_text='Выберите подкатегорию',
                                    verbose_name='подкатегория')
    pair_eu = models.ForeignKey("self", on_delete=models.CASCADE, verbose_name='парный EU-товар', null=True, blank=True)
    no_change = models.BooleanField(verbose_name="Отключены замены", default=False)
    no_limit = models.BooleanField(verbose_name='Безлимитный товар', default=False,
                                   help_text='Поставьте галочку если хотите чтобы товар был безлимитным')

    objects = models.Manager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = '2. Товар'
        verbose_name_plural = '2. Товары'


class BotSettings(models.Model):
    admin_id = models.TextField(verbose_name='ID администраторов', help_text='Будет использован для уведомлений, указывать через перенос.')
    referral_percent = models.PositiveIntegerField(verbose_name='Реферальный %',
                                                   help_text='Общий реферальный % для всех пользователей')
    text_qiwi = models.TextField(null=True, blank=True, max_length=100, verbose_name='Оплата QIWI Текст')
    text_btc = models.TextField(null=True, blank=True, max_length=100, verbose_name='Оплата BTC Текст')
    start_text = models.TextField(verbose_name='Текст для команды /start', max_length=1000,
                                  help_text='Сюда писать текст для команды /start на русском', blank=True)
    help_text = models.TextField(verbose_name='Текст кнопки помощь', max_length=600,
                                 help_text='Сюда писать текст для команды помощь в магазине', blank=True)
    bot_status = models.BooleanField(verbose_name='Статус бота', default=True)

    objects = models.Manager()

    class Meta:
        verbose_name = '5. Настройка бота'
        verbose_name_plural = '5. Настройки бота'

    def __str__(self):
        return 'Настройки бота'


class AllBuyProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.TextField(verbose_name='Название товара')
    count = models.PositiveIntegerField(verbose_name='Количество товара')
    sum = models.PositiveIntegerField(verbose_name='Сумма покупки')
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    objects = models.Manager()

    class Meta:
        verbose_name = '6. Последняя покупка'
        verbose_name_plural = '6. Последнии покупки'

    def __str__(self):
        return f'{self.user} - {self.sum}'


class LogLink(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, verbose_name='Товар')
    link = models.CharField(default='', max_length=100, verbose_name="Локальный путь до лога")
    reg = models.CharField(default='', max_length=3, verbose_name="Регион")

    objects = models.Manager()

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = '7. Загруженные логи'

    def __str__(self):
        return f'{self.link} - {self.product} - {self.reg}'


class Qiwi(models.Model):
    info = models.CharField(max_length=700, blank=True, verbose_name='Номер телефона')
    token = models.CharField(max_length=700, default='0', help_text = 'Токен QIWI API (https://qiwi.com/api)', verbose_name='API-Токен')
    card_num = models.CharField(max_length=700, blank=True, verbose_name='Номер виртуалки')
    active = models.BooleanField(default=True, verbose_name='Активен')
    def __str__(self):
        return f'Qiwi Account: {self.info}'
    class Meta:
        verbose_name = 'кошелёк киви'
        verbose_name_plural = '8. Кошелёк киви'
    
class LogFileID(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.TextField(verbose_name='Название товара')
    log_name = models.TextField(verbose_name='Название лога')
    file_id = models.TextField(verbose_name='ID файла', null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    worked = models.BooleanField(default=False, verbose_name='Заменен?')
    
    class Meta:
        verbose_name = 'купленный лог'
        verbose_name_plural = '9.2. Купленные логи'

    def __str__(self):
        return f'{self.user} - {self.product}'


class Payment(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Пользователь")
    amount = models.IntegerField(default=0, verbose_name="Сумма")
    pay_id = models.CharField(verbose_name="ID Оплаты", default='0',max_length=50)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    class Meta:
        verbose_name = 'пополнение'
        verbose_name_plural = '9. Пополнения'


class PaySystem(models.Model):
    name = models.CharField(max_length=700, blank=True, verbose_name='Название кнопки')
    props = models.TextField(max_length=700, null=True, verbose_name='Реквизиты')
    active = models.BooleanField(default=True, verbose_name='Активен')
    def __str__(self):
        return f'Payment_system: {self.name}'
    class Meta:
        verbose_name = 'вид оплаты'
        verbose_name_plural = '9.1. Платёжки'

class CvvHistory(models.Model):
    card = models.TextField(verbose_name="Строка")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    class Meta:
        verbose_name = 'история'
        verbose_name_plural = '-10. history'