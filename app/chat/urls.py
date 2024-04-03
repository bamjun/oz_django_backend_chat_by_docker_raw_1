# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("room/", views.ChatRoomList.as_view(), name="chatroom-list"),
    path("<int:room_id>/messages", views.ChatMessageList.as_view(), name='message-list'),
    path("<int:room_id>", views.ChatRoomDetail.as_view(), name='chatroom-detail'),
    path('chatting', views.show_html, name='chatting') 
]
