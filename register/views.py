from .forms import CustomRegisterForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from currencyapi.serializers import ConvertedCurrencySerializer
from currencyapi.models import ConvertedCurrency
import requests


@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, username=login_form.cleaned_data['username'],
                                password=login_form.cleaned_data['password'])

            if user is not None:
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
            if form.cleaned_data['currency'] != 'GBP':
                user = CustomUser.objects.get(email=form.cleaned_data['email'])
                url = f"gbp/{form.cleaned_data['currency']}/1000.00"
                absolute_uri = request.build_absolute_uri('/conversion/' + url)
                response = requests.get(absolute_uri)
                if response.status_code == 200:
                    serializer = ConvertedCurrencySerializer(data=response.json())
                    if serializer.is_valid():
                        conversion_response = ConvertedCurrency(serializer.validated_data['amount'],
                                                                serializer.validated_data['is_success'])
                        if conversion_response.is_success:
                            user.account_balance = conversion_response.amount
                            user.save()
                    else:
                        messages.error(request, 'Your currency could not be converted.')
                else:
                    messages.error(request, f"Conversion API returned status code {response.status_code}")
                return redirect('login')
        else:
            messages.error(request, 'Error during registration, please try again.')
            return redirect('register')
    else:
        form = CustomRegisterForm()

    return render(request, 'register/register.html', {'form': form})


@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out')
    return redirect('login')
