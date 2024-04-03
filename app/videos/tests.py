from rest_framework.test import APITestCase
from users.models import User
from .models import Video
from reactions.models import Reaction
from subscriptions.models import Subscription
from django.urls import reverse
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile


class VideoAPITestCase(APITestCase):
    def setUp(self):
        # 유저 생성
        self.user = User.objects.create_user(
            email='test1@example.com',
            password='test123',
        )
        self.client.login(email='test1@example.com', password='test123')

        self.user2 = User.objects.create_user(
            email='test2@example.com',
            password='test123',
        )
        # 비디오 생성
        self.video = Video.objects.create(
            user=self.user,
            link='http://test.com',
            title='test title',
        )

        # Reaction 생성
        self.reaction = Reaction.objects.create(
            user=self.user2, video=self.video, reaction=Reaction.LIKE
            )

        # subscription 생성
        self.sub = Subscription.objects.create(
            subscriber=self.user2, subscribed_to=self.user
            )

    def test_video_list_get(self):
        url = reverse('video-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_video_detail_get(self):
        url = reverse('video-detail', kwargs={'pk': self.video.pk})
        self.client.login(email='test2@example.com', password='test123')

        response = self.client.get(url)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_video_list_post(self):
        url = reverse('video-list')
        data = {
            'user': self.user.pk,
            'link': 'http://test.com',
            'category': 'game',
            'thumbnail': 'http://testthumbnail.com',
            'video_uploaded_url': 'http://testvideoupload.com',
            'video_file': SimpleUploadedFile(
                'file.mp4', b'file_content', content_type='video/mp4'
            ),
            'title': 'test title2',
            'description': 'test description',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_video_detail_put(self):
        url = reverse('video-detail', kwargs={'pk': self.video.pk})
        data = {
            'user': self.user.pk,
            'link': 'http://test.com',
            'category': 'game',
            'thumbnail': 'http://testthumbnail.com',
            'video_uploaded_url': 'http://testvideoupload.com',
            'video_file': SimpleUploadedFile(
                'file.mp4', b'file_content', content_type='video/mp4'
            ),
            'title': 'test title updated',
            'description': 'test description'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test title updated')

    def test_video_detail_delete(self):
        url = reverse('video-detail', kwargs={'pk': self.video.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
