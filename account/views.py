from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from paymentapp.models import PayRequest, Transaction
from django.contrib import messages
from register.models import CustomUser
from decimal import Decimal
import requests
from currencyapi.serializers import ConvertedCurrencySerializer
from currencyapi.models import ConvertedCurrency
from django.db import transaction
from django.utils import timezone


@login_required
def pending_requests(request):
    user = request.user
    received_requests = PayRequest.objects.filter(recipient=user)
    context = {
        'received_requests': received_requests,
    }
    return render(request, 'account/pendingrequests.html', context)


@login_required()
def transaction_history(request):
    user = request.user
    sender_transactions = Transaction.objects.filter(sender=user)
    recipient_transactions = Transaction.objects.filter(recipient=user)
    transactions = sender_transactions | recipient_transactions
    transactions = transactions.order_by('-timestamp')
    return render(request, 'account/transaction_history.html', {'transactions': transactions})


@login_required
@transaction.atomic
def handle_request(request, request_id, action):
    pay_request = get_object_or_404(PayRequest, pk=request_id)
    if pay_request.recipient != request.user:
        return redirect('pendingrequests')
    if action == 'accept':
        recipient = get_object_or_404(CustomUser, username=pay_request.sender)
        amount = pay_request.amount
        sender = request.user
        currency = recipient.currency

        if sender.account_balance < amount:
            messages.error(request, 'Insufficient balance')
            return redirect('pendingrequests')
        if sender.currency != recipient.currency:
            url = f'{sender.currency}/{recipient.currency}/{amount}'
            absolute_uri = request.build_absolute_uri('/conversion/' + url)
            response = requests.get(absolute_uri)
            if response.status_code == 200:
                serializer = ConvertedCurrencySerializer(data=response.json())
                if serializer.is_valid():
                    conversion_response = ConvertedCurrency(serializer.validated_data['amount'],
                                                            serializer.validated_data['is_success'])
                    if conversion_response.is_success:
                        converted_amount = Decimal(conversion_response.amount)
                else:
                    messages.error(request, 'Your currency could not be converted.')
            else:
                messages.error(request, f"Conversion API returned status code {response.status_code}")
        else:
            converted_amount = amount

        # Carry out payments
        sender.account_balance -= amount
        recipient.account_balance += converted_amount
        sender.save()
        recipient.save()

        # Record the transaction in the database
        transaction = Transaction(sender=sender, recipient=recipient, amount=converted_amount, timestamp=timezone.now(),
                                  currency=currency)
        transaction.save()
        pay_request.delete()
        messages.success(request, "Transfer complete")
    elif action == 'reject':
        pay_request.delete()
    return redirect('pendingrequests')
