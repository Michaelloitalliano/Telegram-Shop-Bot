# Generated by Django 3.0.8 on 2020-10-15 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0007_product_cost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product',
            new_name='product_this',
        ),
    ]
