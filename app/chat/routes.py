from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_id>\d+)/chat/', consumers.ChatConsumer.as_asgi()),
    path('ws/chat/<int:room_id>/', consumers.ChatConsumer.as_asgi(), name='chat')
]
# re_path : consumer와 url, view를 연결, 정규 표현식을 사용하는 경우에 씀