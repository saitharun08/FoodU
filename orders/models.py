from django.db import models
from django.conf import settings

class Booking(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('assigned', 'Assigned'),
        ('started', 'Started'),
        ('reached', 'Reached'),
        ('collected', 'Collected'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_bookings'
    )
    partner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='partner_bookings'
    )
    food_item = models.CharField(max_length=100)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.customer.mobile} - {self.status}"
