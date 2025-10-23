from django.db import models
from django.conf import settings


class Booking(models.Model):
    assigned_to = models.ForeignKey(
                    settings.AUTH_USER_MODEL,  
                    on_delete=models.CASCADE,
                    related_name='assigned_bookings' 
                )

    customer = models.ForeignKey(
                    settings.AUTH_USER_MODEL,  
                    on_delete=models.CASCADE,
                    related_name='customer_bookings'
                )
    status = models.CharField(max_length=20, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
