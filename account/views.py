from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from paymentapp.models import PayRequest
from django.contrib import messages


@login_required
def pending_requests(request):
    user = request.user
    received_requests = PayRequest.objects.filter(recipient=user, isPaid=False)
    context = {
        'received_requests': received_requests,
    }
    return render(request, 'account/pendingrequests.html', context)


@login_required
def handle_request(request, request_id, action):
    pay_request = get_object_or_404(PayRequest, pk=request_id)
    if pay_request.recipient != request.user:
        return redirect('pendingrequests')
    if action == 'accept':
        pay_request.isPaid = True
        pay_request.save()
        messages.success(request, "Transfer complete")
    elif action == 'reject':
        pay_request.delete()
    return redirect('pendingrequests')

