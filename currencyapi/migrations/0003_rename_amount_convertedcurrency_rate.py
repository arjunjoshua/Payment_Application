# Generated by Django 4.2 on 2023-04-27 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('currencyapi', '0002_rename_is_valid_convertedcurrency_is_success'),
    ]

    operations = [
        migrations.RenameField(
            model_name='convertedcurrency',
            old_name='amount',
            new_name='rate',
        ),
    ]
