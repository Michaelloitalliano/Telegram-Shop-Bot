# Generated by Django 3.0.8 on 2020-10-12 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0002_botsettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botsettings',
            name='number_qiwi',
            field=models.PositiveIntegerField(verbose_name='Номер киви без +'),
        ),
    ]