from django.urls import path
from . import views

urlpatterns = [
    path('<str:currency1>/<str:currency2>/<str:amount1>/', views.Converter.as_view()),
]