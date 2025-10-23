from django.db import models

class Booking(models.Model):
    customer = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey('auth.User', null=True, blank=True, related_name='assigned_bookings', on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
