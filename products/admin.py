from django.contrib import admin

from products.models import *

# Register your models here.
admin.site.site_header = "Market Admin"
admin.site.site_title = "Market Admin Portal"
admin.site.index_title = "Welcome to the Market Admin Portal"
admin.site.register([
    ProductListing,
    Crop,
    CropCategory  # Uncomment this line to register the ProductListing model
    # Category,  # Uncomment this line to register the Category model
    # Region,  # Uncomment this line to register the Region model
    # UserProfile,  # Uncomment this line to register the UserProfile model
])