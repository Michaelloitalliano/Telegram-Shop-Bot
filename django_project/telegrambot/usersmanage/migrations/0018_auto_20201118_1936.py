# Generated by Django 3.1.1 on 2020-11-18 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0017_allbuyproduct'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.TextField(verbose_name='Локальный путь до лога')),
                ('reg', models.TextField(verbose_name='Регион')),
            ],
            options={
                'verbose_name': '7. Загруженные логи',
                'verbose_name_plural': 'лог',
            },
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'категорию', 'verbose_name_plural': '3. Категория'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name': 'подкатегорию', 'verbose_name_plural': '4. Подкатегория'},
        ),
    ]
