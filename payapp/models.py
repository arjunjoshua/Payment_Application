from django.db import models
from register.models import CustomUser


class Transaction(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_transactions', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=4, default="gbp")

    def __str__(self):
        return f'{self.sender} sent {self.amount} {self.currency} to {self.recipient} on {self.timestamp}'


class PayRequest(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=4, default="gbp")
    isPaid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender} requested for {self.amount} {self.currency} from {self.recipient} on {self.timestamp}'

