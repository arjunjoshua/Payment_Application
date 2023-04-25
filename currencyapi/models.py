from django.db import models


class ConvertedCurrency(models.Model):
    amount = models.FloatField()
    is_success = models.BooleanField(default=False)
    objects = models.Manager()

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, amount, is_success, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.amount = amount
        self.is_success = is_success

