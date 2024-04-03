from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import User


class UserTestCase(APITestCase):
    # 회원가입 테스트 코드 함수
    # 이메일과 패스워드를 입력받아 회원가입이 정상적으로 이루어지는지 확인
    def test_create_user(self):
        email = 'meoyong@gmail.com'
        password = 'password123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        email = 'superM@gmail.com'
        password = 'password123'

        super_user = get_user_model().objects.create_superuser(
            email=email, password=password
        )

        self.assertEqual(super_user.email, email)
        self.assertTrue(super_user.check_password(password))
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)

    def test_login_user(self):
        self.user = User.objects.create_user(email='testemail@gmail.com', password='testpassword')
        url = reverse('login')
        data = {'email': 'testemail@gmail.com', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_logout_user(self):
        self.user = User.objects.create_user(email='testemail@gmail.com', password='testpassword')
        self.client.login(email='testemail@gmail.com', password='testpassword')
        url = reverse('logout')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)

    def test_signup_user(self):
        url = reverse('register')
        data = {'email': 'testemail@gmail.com', 'nickname': 'testnick', 'password': 'testpass', 'password2': 'testpass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)