# chat/views.py
from rest_framework.views import APIView 
from .models import ChatRoom, Message, ChatRoomConnector
from .serializers import ChatRoomSerializer, MessageSerializer, ConnectorSerializer
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from users.models import User
import pdb

def show_html(request):
    return render(request, 'chat/index.html')

class ChatRoomList(APIView):
    def get(self, request):
        # chatroom_list = ChatRoom.objects.filter(member=request.user)
        chatroom_list = ChatRoom.objects.all()
        serializers = ChatRoomSerializer(chatroom_list, many=True)

        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        user_data = request.data
        room_serializer = ChatRoomSerializer(data=user_data)
        if room_serializer.is_valid():
            # 채팅방 db에 저장
            chatroom = room_serializer.save()
                # 유저의 참여 상태를 db에 저장
            ChatRoomConnector.objects.create(user=request.user, chatroom=chatroom)
            return Response(
                room_serializer.data, status=status.HTTP_201_CREATED
            )
           

        return Response(
            room_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class ChatRoomDetail(APIView):
    def post(self, request, room_id):
        # user_data = request.data
        # 채팅방의 유무 확인
        chatroom = get_object_or_404(ChatRoom, id=room_id)
        # 채팅방에 유저를 커넥터로 참여시키기
        ChatRoomConnector.objects.create(user=request.user, chatroom=chatroom)

        return Response(
            status=status.HTTP_201_CREATED
        )

    def get(self, request, room_id):
        chatroom = get_object_or_404(ChatRoom, id=room_id)
        chatroom_serializer = ChatRoomSerializer(chatroom)
        members = ChatRoomConnector.objects.filter(chatroom=room_id)
        members_serializer = ConnectorSerializer(members, many=True)
        data = {
            'chatroom': chatroom_serializer.data,
            'members': members_serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)


    
class ChatMessageList(APIView):
    def post(self, request, room_id):
        user_data = request.data
        serializer = MessageSerializer(data=user_data)
        chatroom = get_object_or_404(ChatRoom, id=room_id)

        if serializer.is_valid():
            serializer.save(sender=request.user, chatroom=chatroom)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, room_id):
        messages = Message.objects.filter(chatroom=room_id).order_by('created_at')[:30]
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)