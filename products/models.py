from django.db import models
from accounts.models import User
from django.utils.text import slugify
import uuid


def generate_uid():
    return uuid.uuid4().hex[:22]

class CropCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Crop categories"

class Crop(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(CropCategory, on_delete=models.CASCADE, related_name='crops')
    common_units = models.CharField(max_length=100, help_text="Common units for this crop, e.g., 'kg, bag, crate'")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class ProductListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='listings')
    uid = models.CharField(max_length=22, unique=True, editable=False, default=generate_uid)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    region = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    harvest_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='product_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    whatsapp_click_count = models.IntegerField(default=0)
    
    @property
    def slug(self):
        return self.crop.slug
    
    def __str__(self):
        return f"{self.crop.name} - {self.quantity} {self.unit}"
    
