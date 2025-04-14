from django.db import models
from accounts.models import User

class TransporterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=50)
    route_regions = models.TextField()
    pricing_note = models.TextField()
    contact_number = models.CharField(max_length=20)
    is_available = models.BooleanField(default=True)