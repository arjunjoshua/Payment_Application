from rest_framework import serializers
from .models import ConvertedCurrency


class ConvertedCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvertedCurrency
        fields = ["rate", "is_success"]