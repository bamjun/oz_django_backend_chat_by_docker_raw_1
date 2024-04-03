from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from videos.models import Video
from .models import Reaction
from django.urls import reverse


class ReactionAPITestCase(APITestCase):
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
            title='test title2',
        )
        print(self.video)

    def test_reaction_detail_post(self):
        url = reverse('video-reaction', kwargs={'video_id': self.video.pk})
        data = {
            'reaction': Reaction.LIKE
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reaction.objects.count(), 1)
        self.assertEqual(
            Reaction.objects.get().reaction,
            Reaction.LIKE
        )
