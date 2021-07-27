# Generated by Django 3.1.1 on 2020-11-18 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0018_auto_20201118_1936'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loglink',
            options={'verbose_name': 'лог', 'verbose_name_plural': '7. Загруженные логи'},
        ),
        migrations.AlterField(
            model_name='loglink',
            name='link',
            field=models.CharField(default='', max_length=100, verbose_name='Локальный путь до лога'),
        ),
        migrations.AlterField(
            model_name='loglink',
            name='reg',
            field=models.CharField(default='', max_length=3, verbose_name='Регион'),
        ),
    ]