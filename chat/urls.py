from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('history/<int:booking_id>/', views.history, name='chat_history')
]
