# Generated by Django 3.1.2 on 2020-11-23 10:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0023_auto_20201123_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allbuyproduct',
            name='create_date',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Дата'),
        ),
    ]