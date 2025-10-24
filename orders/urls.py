from django.urls import path
from django.http import HttpResponse
from . import views

def placeholder_view(request):
    return HttpResponse("Orders placeholder")

urlpatterns = [
    # Customer
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/create/', views.create_booking, name='create_booking'),
    path('customer/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    # Admin
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Partner
    path('partner/dashboard/', views.partner_dashboard, name='partner_dashboard'),
    path('partner/update/<int:booking_id>/', views.update_status, name='update_status')
]
