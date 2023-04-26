from . import views
from django.urls import path

urlpatterns = [
    path("pendingrequests/", views.pending_requests, name="pendingrequests"),
    path('requests/<int:request_id>/<str:action>/', views.handle_request, name='handle_request'),
    path("transaction_history", views.transaction_history, name="transaction_history"),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark_as_read/', views.mark_as_read, name='mark_as_read'),
]