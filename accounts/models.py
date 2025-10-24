from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (('customer','Customer'), ('partner','Delivery Partner'), ('admin','Admin'))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    mobile = models.CharField(max_length=15, unique=True)

    username = models.CharField(max_length=150, unique=False, blank=True, null=True)

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []  # No username or email required

    def __str__(self):
        return f"{self.mobile} ({self.role})"
