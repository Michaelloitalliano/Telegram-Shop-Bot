# Generated by Django 3.1.2 on 2020-11-23 10:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0021_allbuyproduct_create_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allbuyproduct',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 23, 10, 44, 5, 283571), verbose_name='Создан'),
        ),
    ]
