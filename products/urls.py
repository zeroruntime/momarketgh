from django.urls import path
from . import views
# from .views import market_view

# urlpatterns = [
#     path('market/', market_view, name='market'),

#     # Product listings
#     path('create-listing/', views.create_listing, name='create_listing'),
#     path('products/<slug:slug>-<str:uid>/', views.product_detail, name='product_detail'),


#     # path('', views.product_list, name='product_list'),
#     # path('create/', views.product_create, name='product_create'),
#     # path('<int:pk>/', views.product_detail, name='product_detail'),
#     # path('<int:pk>/update/', views.product_update, name='product_update'),
#     # path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    
#     # # Categories/regions
#     # path('category/<slug:category>/', views.product_by_category, name='product_by_category'),
#     # path('region/<slug:region>/', views.product_by_region, name='product_by_region'),
    
#     # # WhatsApp integration
#     # path('<int:pk>/contact/', views.whatsapp_contact, name='whatsapp_contact'),
# ]

urlpatterns = [
    path('market/', views.crop_categories, name='market'),
    path('crop/<slug:crop_slug>/', views.crop_listings, name='crop_listings'),
    path('api/track-whatsapp-click/', views.track_whatsapp_click, name='track_whatsapp_click'),
    path('create-listing/', views.create_listing, name='create_listing'),
    path('products/<slug:slug>-<str:uid>/', views.product_detail, name='product_detail'),


]