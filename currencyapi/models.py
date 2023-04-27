from django.db import models


class ConvertedCurrency(models.Model):
    rate = models.DecimalField(decimal_places=2, max_digits=4)
    is_success = models.BooleanField(default=False)
    objects = models.Manager()

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, amount, is_success, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rate = amount
        self.is_success = is_success

