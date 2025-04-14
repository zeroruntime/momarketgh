from django.urls import path
from . import views

urlpatterns = [
    # # Custom admin views
    # path('', views.admin_dashboard, name='admin_dashboard'),
    # path('pending-listings/', views.pending_listings, name='pending_listings'),
    # path('user-management/', views.user_management, name='user_management'),
    # path('price-settings/', views.price_settings, name='price_settings'),
    
    # # Moderation actions
    # path('approve-listing/<int:pk>/', views.approve_listing, name='approve_listing'),
    # path('flag-user/<int:pk>/', views.flag_user, name='flag_user'),
]