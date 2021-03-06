# Generated by Django 3.0.8 on 2020-10-13 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0004_auto_20201013_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botsettings',
            name='help_text_en',
            field=models.TextField(blank=True, help_text='Сюда писать текст для команды /start на английском', max_length=1000, verbose_name='Текст кнопки помощь'),
        ),
        migrations.AlterField(
            model_name='botsettings',
            name='help_text_ru',
            field=models.TextField(blank=True, help_text='Сюда писать текст для команды /start на русском', max_length=1000, verbose_name='Текст кнопки помощь'),
        ),
        migrations.AlterField(
            model_name='botsettings',
            name='number_qiwi',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Номер киви без +'),
        ),
        migrations.AlterField(
            model_name='botsettings',
            name='start_text_en',
            field=models.TextField(blank=True, help_text='Сюда писать текст для команды /start на английском', max_length=1000, verbose_name='Текст для команды /start'),
        ),
        migrations.AlterField(
            model_name='botsettings',
            name='start_text_ru',
            field=models.TextField(blank=True, help_text='Сюда писать текст для команды /start на английском', max_length=1000, verbose_name='Текст для команды /start'),
        ),
        migrations.AlterField(
            model_name='botsettings',
            name='token_qiwi',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='Токен от киви'),
        ),
    ]
