from .forms import PaymentForm, RequestForm
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Transaction, PayRequest
from register.models import CustomUser
from decimal import Decimal
import requests
from currencyapi.serializers import ConvertedCurrencySerializer
from currencyapi.models import ConvertedCurrency


@login_required(login_url='/login')
@transaction.atomic
def make_payment(request):
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            recipient_username = payment_form.cleaned_data['username']
            recipient = get_object_or_404(CustomUser, username=recipient_username)
            amount = Decimal(request.POST.get('amount'))
            sender = request.user
            currency = recipient.currency

            # Ensure that the sender has enough balance to make the payment
            if sender.account_balance < amount:
                messages.error(request, 'Insufficient balance')
                return redirect('payuser')

            if sender.currency != recipient.currency:
                url = f'{sender.currency}/{recipient.currency}/{amount}'
                absolute_uri = request.build_absolute_uri('/conversion/' + url)
                response = requests.get(absolute_uri)
                if response.status_code == 200:
                    serializer = ConvertedCurrencySerializer(data=response.json())
                    if serializer.is_valid():
                        conversion_response = ConvertedCurrency(serializer.validated_data['rate'],
                                                                serializer.validated_data['is_success'])
                        if conversion_response.is_success:
                            converted_amount = conversion_response.rate * amount
                            converted_amount = Decimal(converted_amount)
                    else:
                        messages.error(request, 'Your currency could not be converted.')
                else:
                    messages.error(request, f"Conversion API returned status code {response.status_code}")
            else:
                converted_amount = amount

            # Deduct the amount from the sender's account and credit it to the recipient's account
            sender.account_balance -= amount
            recipient.account_balance += converted_amount
            sender.save()
            recipient.save()

            # Record the transaction in the database
            transaction = Transaction(sender=sender, recipient=recipient, amount=converted_amount, timestamp=timezone.now(), currency=currency)
            transaction.save()

            # Return a success message to the user
            messages.success(request, 'Payment successful')
            return redirect('home')

        else:
            messages.error(request, "The selected user does not exist")
            return redirect('payuser')
    else:
        payment_form = PaymentForm()

    return render(request, 'payment/payuser.html', {'form': payment_form},)


@login_required(login_url='/login')
@transaction.atomic
def request_payment(request):
    if request.method == 'POST':
        request_form = RequestForm(request.POST)
        if request_form.is_valid():
            recipient_username = request_form.cleaned_data['username']
            recipient = get_object_or_404(CustomUser, username=recipient_username)
            amount = Decimal(request.POST.get('amount'))
            sender = request.user
            currency = recipient.currency

            # Call the currency API to convert currency if required
            if sender.currency != recipient.currency:
                url = f'{sender.currency}/{recipient.currency}/{amount}'
                absolute_uri = request.build_absolute_uri('/conversion/' + url)
                response = requests.get(absolute_uri)
                if response.status_code == 200:
                    serializer = ConvertedCurrencySerializer(data=response.json())
                    if serializer.is_valid():
                        conversion_response = ConvertedCurrency(serializer.validated_data['rate'],
                                                                serializer.validated_data['is_success'])
                        if conversion_response.is_success:
                            converted_amount = amount * conversion_response.rate
                            converted_amount = Decimal(converted_amount)
                    else:
                        messages.error(request, 'Your currency could not be converted.')
                else:
                    messages.error(request, f"Conversion API returned status code {response.status_code}")
            else:
                converted_amount = amount

            # record the request in the database
            requested = PayRequest(sender=sender, recipient=recipient, amount=converted_amount, timestamp=timezone.now(), currency=currency)
            requested.save()

            # display a success message to the user
            messages.success(request, f'Request has been sent to {recipient_username}')
            return redirect('home')

        else:
            messages.error(request, "The selected user does not exist")
            return redirect('payrequest')
    else:
        request_form = RequestForm()

    return render(request, 'payment/payrequest.html', {'form': request_form})



