from .forms import CustomRegisterForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from currencyapi.serializers import ConvertedCurrencySerializer
from currencyapi.models import ConvertedCurrency
import requests
from account.models import Notification


@login_required(login_url='/login')
def home(request):
    # Retrieve the user's unread notifications
    notifications = Notification.objects.filter(user=request.user, unread=True)

    # Render the dashboard template with the user's pay requests, transactions, and notifications
    context = {
        'notifications': notifications,
    }
    return render(request, 'home.html', context)


def login_page(request):
    # Redirect standard users to the acccount home page and superusers to the admin home page
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_home')
    elif request.user.is_authenticated and not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, username=login_form.cleaned_data['username'],
                                password=login_form.cleaned_data['password'])

            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_home')
            elif user is not None and not user.is_staff:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username or password incorrect!')
    else:
        login_form = LoginForm()

    return render(request, 'register/login.html', {'form': login_form})


def register_page(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New account created successfully')

            # Call the currencyapi if the selected currency isn't GBP
            if form.cleaned_data['currency'] != 'GBP':
                user = CustomUser.objects.get(username=form.cleaned_data['username'])
                url = f"GBP/{form.cleaned_data['currency']}/1000.00"
                absolute_uri = request.build_absolute_uri('/conversion/' + url)
                response = requests.get(absolute_uri)
                if response.status_code == 200:
                    serializer = ConvertedCurrencySerializer(data=response.json())
                    if serializer.is_valid():
                        conversion_response = ConvertedCurrency(serializer.validated_data['rate'],
                                                                serializer.validated_data['is_success'])
                        if conversion_response.is_success:
                            user.account_balance = conversion_response.rate * 1000
                            user.save()
                    else:
                        messages.error(request, 'Your currency could not be converted.')
                else:
                    messages.error(request, f"Conversion API returned status code {response.status_code}")
                return redirect('login')
        else:
            messages.error(request, 'Error during registration, please try again.')
    else:
        form = CustomRegisterForm()

    return render(request, 'register/register.html', {'form': form})


@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect('login')
