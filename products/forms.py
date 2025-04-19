from django import forms
from .models import ProductListing, Crop

class ProductListingForm(forms.ModelForm):
    class Meta:
        model = ProductListing
        fields = [
            'crop', 'description', 'quantity', 'unit', 'price_per_unit',
            'region', 'location', 'harvest_date', 'photo'
        ]
        widgets = {
            'harvest_date': forms.DateInput(attrs={'type': 'date'}),
        }
