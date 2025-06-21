from django.contrib import admin
from accounts.models import User  # Import the User model
# Register your models here.
admin.site.register(User)  # Register the User model with the admin site