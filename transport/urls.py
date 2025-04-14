from django.urls import path
from . import views

urlpatterns = [
    # # Transporter profiles
    # path('transporters/', views.transporter_list, name='transporter_list'),
    # path('transporter/<int:pk>/', views.transporter_detail, name='transporter_detail'),
    # path('transporter-profile/', views.transporter_profile, name='transporter_profile'),
    # path('transporter-profile/update/', views.transporter_profile_update, name='transporter_profile_update'),
    
    # # Delivery requests (future feature)
    # path('delivery-requests/', views.delivery_requests, name='delivery_requests'),
]