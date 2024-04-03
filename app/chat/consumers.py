import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

import django
django.setup()

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from users.models import User
from chat.models import Message, ChatRoom, ChatRoomConnector
from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.response import Response


class ChatConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def new_chat(self, message):
        chatroom = get_object_or_404(ChatRoom, id=self.room_id)
        sender = get_object_or_404(User, id=self.user_id)
        
        Message.objects.create(sender=sender, message=message, chatroom=chatroom)
    
    @sync_to_async
    def get_connector(self):
        return ChatRoomConnector.objects.filter(user=self.user_id, chatroom=self.room_id).first()
    
    @sync_to_async
    def status_changer(self, connector):
        connector.status = not connector.status
        connector.save()

    @sync_to_async
    def create_connector(self):
        chatroom = get_object_or_404(ChatRoom, id=self.room_id)
        user = get_object_or_404(User, id=self.user_id)

        return ChatRoomConnector.objects.create(
            chatroom=chatroom, user=user
        )
    
    # 소켓에 연결
    async def connect(self):
        try:
            self.room_id = self.scope['url_route']['kwargs']['room_id']
            self.user_id = self.scope['user'].id
            self.chat_group_name = 'chat_' + str(self.room_id)
        except Exception as e:
            return Response(
                {'msg': str(e)}, status=status.HTTP_404_NOT_FOUND
            )
        
        self.connector = await self.get_connector()

        if not self.connector:
            self.connector = await self.create_connector()

        if self.connector.status:
            await self.close()

        else:
            await self.channel_layer.group_add(
                self.chat_group_name,
                self.channel_name
            )
            await self.status_changer(self.connector)
            await self.accept()

    # 메시지 받는 부분
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            msg = text_data_json.get('message')
            user_email = text_data_json.get('user_email')
        except Exception as e:
            return Response(
                {'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': msg,
                'user_email': user_email,
            }
        )
        await self.new_chat(message=msg)

    # 소켓 연결 해제
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )
        await self.status_changer(self.connector)

    # 그룹으로부터 받은 메시지를 클라이언트에 전달하는 역할
    async def chat_message(self, event):
        msg = event['message']
        user_email = event['user_email']

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': msg,
            'user_email': user_email
        }))

# get -> text_data 했을때 검증
# room_id 제대로 가져오는 지 검증
# 그룹네임의 존재여부
# 커넥트 retry