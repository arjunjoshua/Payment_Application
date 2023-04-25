from rest_framework import serializers
from .models import ConvertedCurrency


class ConvertedCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvertedCurrency
        fields = ["amount", "is_success"]