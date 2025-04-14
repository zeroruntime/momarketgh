from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Farmer', 'Farmer'),
        ('Trader', 'Trader'),
        ('Transporter', 'Transporter'),
    ]
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    region = models.CharField(max_length=100)
    location = models.CharField(max_length=255)