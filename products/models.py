from django.db import models
from accounts.models import User
from django.utils.text import slugify
import uuid


def generate_uid():
    return uuid.uuid4().hex[:22]

class ProductListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    uid = models.CharField(max_length=22, unique=True, editable=False)
    description = models.TextField()
    quantity = models.FloatField()
    unit = models.CharField(max_length=50)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    region = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='product_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4().hex[:22]

        if not self.slug:
            base_slug = slugify(self.crop_name)
            slug = base_slug
            num = 1
            while ProductListing.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.crop_name


class ProductPhoto(models.Model):
    product_listing = models.ForeignKey(ProductListing, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='product_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.product_listing.crop_name}"
