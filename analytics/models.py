from django.db import models
from products.models import ProductListing
from accounts.models import User

class WhatsAppClick(models.Model):
    listing = models.ForeignKey(ProductListing, on_delete=models.CASCADE)
    clicked_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)

class PriceHistory(models.Model):
    crop_name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    average_price = models.DecimalField(max_digits=10, decimal_places=2)
    calculated_on = models.DateField()