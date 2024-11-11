from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from ..serializers import UserSerializer, MyTokenObtainPairSerializer

class TestUserSerializer(TestCase):
    def test_user_serializer_create(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'testuser@example.com'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, data['username'])
        self.assertTrue(user.check_password(data['password']))
        self.assertEqual(user.email, data['email'])

    def test_user_serializer_missing_email(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_user_serializer_empty_email(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': ''
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

class TestMyTokenObtainPairSerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com',
            is_staff=True
        )

    def test_token_obtain_pair_serializer(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        serializer = MyTokenObtainPairSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        tokens = serializer.validated_data
        self.assertIn('access', tokens)
        self.assertIn('refresh', tokens)

        access_token = tokens['access']
        token = AccessToken(access_token)
        self.assertEqual(token['username'], 'testuser')
        self.assertEqual(token['is_staff'], self.user.is_staff)


    def test_token_obtain_pair_serializer_invalid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        serializer = MyTokenObtainPairSerializer(data=data)
        
        with self.assertRaises(AuthenticationFailed) as context:
            serializer.is_valid(raise_exception=True)
        
        self.assertEqual(
            str(context.exception),
            'No active account found with the given credentials'
        )
