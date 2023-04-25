# Generated by Django 4.2 on 2023-04-25 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0005_alter_customuser_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='currency',
            field=models.CharField(blank=True, choices=[('eur', 'EUR'), ('usd', 'USD'), ('gbp', 'GBP')], max_length=4),
        ),
    ]
