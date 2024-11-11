from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from reviews.models import Review

class ReviewViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_create_url = reverse('review-list-create')
        self.detail_url_name = 'review-detail'
        self.user = User.objects.create_user(
            username='testuser', password='testpass123', email='testuser@example.com'
        )
        self.admin_user = User.objects.create_user(
            username='adminuser', password='adminpass123', email='admin@example.com', is_staff=True
        )
        self.review = Review.objects.create(
            title='Test Review',
            content='This is a test review.',
            framework_name='Django',
            framework_version='3.2',
            author=self.user
        )

    def test_review_list_view(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Review')

    def test_review_create_view_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'title': 'New Review',
            'content': 'This is a new review.',
            'framework_name': 'Flask',
            'framework_version': '2.0',
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        new_review = Review.objects.get(title='New Review')
        self.assertEqual(new_review.author, self.admin_user)

    def test_review_create_view_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Unauthorized Review',
            'content': 'This should not be allowed.',
            'framework_name': 'Django',
            'framework_version': '3.2',
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_detail_view(self):
        detail_url = reverse(self.detail_url_name, args=[self.review.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Review')

    def test_review_update_view_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        detail_url = reverse(self.detail_url_name, args=[self.review.id])
        data = {'title': 'Updated Review'}
        response = self.client.patch(detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.title, 'Updated Review')

    def test_review_update_view_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        detail_url = reverse(self.detail_url_name, args=[self.review.id])
        data = {'title': 'Attempted Update'}
        response = self.client.patch(detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_delete_view_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        detail_url = reverse(self.detail_url_name, args=[self.review.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_review_delete_view_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        detail_url = reverse(self.detail_url_name, args=[self.review.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
