# Generated by Django 4.2 on 2023-04-24 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('currencyapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='convertedcurrency',
            old_name='is_valid',
            new_name='is_success',
        ),
    ]
