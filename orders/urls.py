from django.urls import path
from . import views

urlpatterns = [
    # Customer URLs
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/create/', views.create_booking, name='create_booking'),
    path('customer/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/assign/<int:booking_id>/', views.assign_partner, name='assign_partner'),  # 👈 Added

    # Partner URLs
    path('partner/dashboard/', views.partner_dashboard, name='partner_dashboard'),
    path('partner/update/<int:booking_id>/', views.update_status, name='update_status'),
]
