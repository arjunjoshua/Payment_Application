from . import views
from django.urls import path

urlpatterns = [
    path("payuser/", views.make_payment, name="payuser"),
    path("payrequest/", views.request_payment, name="payrequest"),
]
