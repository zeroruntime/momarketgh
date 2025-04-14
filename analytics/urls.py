from django.urls import path
from . import views

urlpatterns = [
    # # Farmer analytics
    path('farmer-dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    # path('my-listings-stats/', views.my_listings_stats, name='my_listings_stats'),
    
    # # Price dashboard
    # path('price-dashboard/', views.price_dashboard, name='price_dashboard'),
    # path('price-history/<str:crop>/', views.price_history, name='price_history'),
    
    # # Market trends
    # path('market-trends/', views.market_trends, name='market_trends'),
]