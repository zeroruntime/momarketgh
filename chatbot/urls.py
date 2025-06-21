from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('chat/', views.chat_with_kwasi, name='chat'),
    path('widget/', views.chatbot_widget, name='widget'),
]