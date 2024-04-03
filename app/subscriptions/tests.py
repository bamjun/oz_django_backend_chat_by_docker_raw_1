from rest_framework.test import APITestCase
from users.models import User
from .models import Subscription
from django.urls import reverse
from rest_framework import status


class TestSubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword123'
        )
        self.user2 = User.objects.create_user(
            email='testuser2@example.com',
            password='testpassword123'
        )
        self.client.login(
            email='testuser@example.com',
            password='testpassword123'
        )

    def test_sub_list_post(self):
        url = reverse('subs-list')
        data = {
            'subscribed_to': self.user2.pk,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(
            Subscription.objects.get().subscribed_to,
            self.user2
        )

    def test_sub_detail_delete(self):
        Subscription.objects.create(
            subscriber=self.user1, subscribed_to=self.user2
        )
        url = reverse('subs-detail', kwargs={'pk': self.user2.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.count(), 0)
