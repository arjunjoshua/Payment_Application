from . import views
from django.urls import path

urlpatterns = [
    path("pendingrequests/", views.pending_requests, name="pendingrequests"),
    path('requests/<int:request_id>/<str:action>/', views.handle_request, name='handle_request'),
]