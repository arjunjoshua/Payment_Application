from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


CURRENCY_CHOICES = {
    ('gbp', 'GBP'),
    ('usd', 'USD'),
    ('eur', 'EUR'),
}


class CustomUser(AbstractUser):
    username = models.CharField(unique=True, max_length=32, default='blank_user')
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    account_balance = models.DecimalField(max_digits=15, default=1000, decimal_places=2, blank=True)
    currency = models.CharField(max_length=4, choices=CURRENCY_CHOICES, blank=True)

    objects = CustomUserManager()

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username



