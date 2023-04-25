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
        conversion_rate = {
            'gbp_usd': 1.37,
            'gbp_eur': 1.16,
            'usd_gbp': 0.73,
            'usd_eur': 0.84,
            'eur_gbp': 0.86,
            'eur_usd': 1.19
        }
        amount1 = float(self.kwargs.get('amount1'))
        amount2 = decimal.Decimal(0.00)
        conversion_rate_key = f"{currency1}_{currency2}"
        if conversion_rate_key in conversion_rate:
            amount2 = amount1 * conversion_rate[conversion_rate_key]
        else:
            is_success = False

        response = ConvertedCurrencySerializer(ConvertedCurrency(amount2, is_success))

        return Response(response.data)
