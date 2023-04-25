from django.contrib import admin
from .models import Transaction, PayRequest

admin.site.register(Transaction)
admin.site.register(PayRequest)
