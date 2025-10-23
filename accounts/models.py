from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (('customer','Customer'), ('partner','Delivery Partner'), ('admin','Admin'))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    mobile = models.CharField(max_length=20, blank=True, null=True)
