# Generated by Django 3.0.8 on 2020-10-16 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0008_auto_20201015_1712'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='locale',
        ),
    ]