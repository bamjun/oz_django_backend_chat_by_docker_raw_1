from rest_framework.serializers import ModelSerializer
from .models import ChatRoom, Message, ChatRoomConnector

class ChatRoomSerializer(ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'chatroom']
        depth = 1 

class ConnectorSerializer(ModelSerializer):
    class Meta:
        model = ChatRoomConnector
        fields = '__all__'
        depth = 1