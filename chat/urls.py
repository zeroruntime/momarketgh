from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('start/<str:product_uid>/', views.start_chat, name='start_chat'),
    path('conversation/<uuid:uuid>/', views.conversation_detail, name='conversation_detail'),
    path('send-message/', views.send_message, name='send_message'),
    path('api/messages/<uuid:uuid>/', views.get_messages, name='get_messages'),
]