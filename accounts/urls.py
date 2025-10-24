from django.urls import path
from django.http import HttpResponse
from . import views


urlpatterns = [
    path('login/', views.mobile_login, name='mobile_login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('unauthorized/', views.unauthorized, name='unauthorized')
]
