# Generated by Django 3.0.8 on 2020-10-16 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0011_auto_20201016_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botsettings',
            name='help_text_auto_guarantor',
            field=models.TextField(blank=True, help_text='Сюда писать текст для команды помощь в авто-гаранте', max_length=600, verbose_name='Текст кнопки помощь'),
        ),
        migrations.AlterField(
            model_name='botsettings',
            name='help_text_shop',
            field=models.TextField(blank=True, help_text='Сюда писать текст для команды помощь в магазине', max_length=600, verbose_name='Текст кнопки помощь'),
        ),
    ]
