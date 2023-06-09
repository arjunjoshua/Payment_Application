from django.urls import include, path
from django.contrib import admin
from register import views

urlpatterns = [
    path("", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path('home/', views.home, name="home"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_user, name='logout'),
    path("conversion/", include('currencyapi.urls')),
    path("payapp/", include('payapp.urls')),
    path("account/", include('account.urls')),
    path('admin/', admin.site.urls),
    path('administration/', include('administration.urls')),
]
