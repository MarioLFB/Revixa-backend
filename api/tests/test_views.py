from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

class TestCreateUserView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')

    def test_create_user(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'testuser@example.com'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

class TestMyTokenObtainPairView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('token_obtain_pair')
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_obtain_token(self):
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

class TestUserProfileView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user_profile')
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_get_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

class TestUpdateEmailView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('update_email')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='old@example.com'
        )

    def test_update_email(self):
        self.client.force_authenticate(user=self.user)
        data = {'email': 'new@example.com'}
        response = self.client.put(self.url, data, format='json')
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, 'new@example.com')

class TestUpdatePasswordView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('update_password')
        self.user = User.objects.create_user(username='testuser', password='oldpass123')

    def test_update_password(self):
        self.client.force_authenticate(user=self.user)
        data = {'current_password': 'oldpass123', 'new_password': 'newpass123'}
        response = self.client.put(self.url, data, format='json')
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password('newpass123'))
