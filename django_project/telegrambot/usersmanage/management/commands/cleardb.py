from django.core.management import BaseCommand

from django_project.telegrambot.usersmanage.models import *


class Command(BaseCommand):
    help = 'clear db'

    def handle(self, *args, **kwargs):
        User.objects.all().delete()
        SubCategory.objects.all().delete()
        Category.objects.all().delete()
        Product.objects.all().delete()
        BotSettings.objects.all().delete()
        BotSettings.objects.create(referral_percent=10)
        print('Чистка базы данных выполнена успешно')