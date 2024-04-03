from rest_framework.test import APITestCase
from users.models import User
from .models import ChatRoom, ChatRoomConnector, Message
from rest_framework import status
from django.urls import reverse
import pdb

class ChatRoomTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123'
        )
        self.client.login(
            email='testuser@example.com',
            password='testpassword123'
        )

    def test_chatroom_list_get(self):
        chatroom = ChatRoom.objects.create(
            roomname='test_chatroom'
        )
        ChatRoomConnector.objects.create(
            user = self.user, chatroom = chatroom
        )
        url = reverse('chatroom-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chatroom_list_post(self):
        data = {
            'roomname': 'test_chatroom'
        }
        url = reverse('chatroom-list')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChatRoom.objects.count(), 1)

    def test_chatroom_detail_get(self):
        chatroom = ChatRoom.objects.create(
            roomname='test_chatroom'
        )
        ChatRoomConnector.objects.create(
            user = self.user, chatroom = chatroom
        )
        url = reverse('chatroom-detail', kwargs={'room_id': chatroom.id})

        response = self.client.get(url)
        pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_chatroom_detail_post(self):
        chatroom = ChatRoom.objects.create(
            roomname='test_chatroom'
        )
        print(chatroom.id)

        ChatRoomConnector.objects.create(
            user = self.user, chatroom = chatroom
        )
        self.user2 = User.objects.create(
            email='testuser2@example.com',
            password='testpassword123'
        )
        self.client.login(
            email='testuser2@example.com',
            password='testpassword1234'
        )
        url = reverse('chatroom-detail', kwargs={'room_id': chatroom.id})

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)