from rest_framework.test import APITestCase
from users.models import User
from videos.models import Video
from .models import Comment
from rest_framework import status
from django.urls import reverse


class CommentAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123'
        )
        self.client.login(
            email='testuser@example.com',
            password='testpassword123'
        )
        self.video = Video.objects.create(
            user=self.user,
            link='http://test.com',
            title='test title',
        )

    def test_create_comment(self):
        url = reverse('video-comment', kwargs={'video_id': self.video.id})
        data = {
            'content': 'test comment'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_get_comment_list(self):
        Comment.objects.create(
            user=self.user,
            video=self.video,
            content='test comment'
        )
        url = reverse('video-comment', kwargs={'video_id': self.video.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
