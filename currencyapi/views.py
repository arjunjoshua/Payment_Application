from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ConvertedCurrency
from .serializers import ConvertedCurrencySerializer
import decimal


class Converter(APIView):
    def get(self, *args, **kwargs):
        is_success = True
        currency1 = self.kwargs.get('currency1')
        currency2 = self.kwargs.get('currency2')
        # check the currencies against the dictionary and return rate if applicable
        conversion_rate = {
            'GBP_USD': 1.37,
            'GBP_EUR': 1.16,
            'USD_GBP': 0.73,
            'USD_EUR': 0.84,
            'EUR_GBP': 0.86,
            'EUR_USD': 1.19
        }
        rate = 0.0
        conversion_rate_key = f"{currency1}_{currency2}"
        if conversion_rate_key in conversion_rate:
            rate = conversion_rate[conversion_rate_key]
        else:
            is_success = False

        response = ConvertedCurrencySerializer(ConvertedCurrency(rate, is_success))

        return Response(response.data)
