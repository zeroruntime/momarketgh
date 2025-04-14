from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.CustomLoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # Registration
    path('register/', views.register, name='register'),
    
    # Profiles
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    
    # Role-specific views
    # path('farmers/', views.farmer_list, name='farmer_list'),
    # path('traders/', views.trader_list, name='trader_list'),
    # path('transporters/', views.transporter_list, name='transporter_list'),
]