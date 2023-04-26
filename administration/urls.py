from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.admin_home, name="admin_home"),
    path("view_accounts/", views.admin_view_accounts, name="view_accounts"),
    path("view_transactions", views.admin_view_transactions, name="view_transactions"),
    path("register_admin", views.register_admin, name="register_admin"),
]