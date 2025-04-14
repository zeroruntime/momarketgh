from django import forms
from .models import ProductListing

class ProductListingForm(forms.ModelForm):
    class Meta:
        model = ProductListing
        fields = [
            'crop_name', 'description', 'quantity', 'unit',
            'price_per_unit', 'region', 'location', 'photo'
        ]
