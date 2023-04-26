from django.db import models
from register.models import CustomUser


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)
    url = models.CharField(max_length=255, default="/home")

    def __str__(self):
        return f'{self.user} - {self.message}'
