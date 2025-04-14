from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('about/', views.about, name='about'),
    # path('contact/', views.contact, name='contact'),
    # path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    # path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    # path('faq/', views.faq, name='faq'),
]

