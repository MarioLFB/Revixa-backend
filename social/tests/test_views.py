from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from reviews.models import Review
from social.models import Post, Like

class PostViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2', password='testpass123'
        )
        self.review = Review.objects.create(
            title='Test Review',
            content='This is a test review.',
            framework_name='Django',
            author=self.user
        )
        self.post = Post.objects.create(
            content='This is a test post.',
            author=self.user,
            review=self.review
        )
        self.post_url = reverse('post-detail', args=[self.post.id])
        self.list_create_url = reverse('review-post-list-create', args=[self.review.id])
        self.like_url = reverse('like-post', args=[self.post.id])

    def test_post_list_view(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], 'This is a test post.')

    def test_post_create_view_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {'content': 'New post content.'}
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        new_post = Post.objects.get(id=response.data['id'])
        self.assertEqual(new_post.content, data['content'])
        self.assertEqual(new_post.author, self.user)
        self.assertEqual(new_post.review, self.review)

    def test_post_create_view_unauthenticated(self):
        data = {'content': 'New post content.'}
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_detail_view(self):
        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'This is a test post.')

    def test_post_update_view_owner(self):
        self.client.force_authenticate(user=self.user)
        data = {'content': 'Updated post content.'}
        response = self.client.patch(self.post_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, data['content'])

    def test_post_update_view_non_owner(self):
        self.client.force_authenticate(user=self.user2)
        data = {'content': 'Attempted update content.'}
        response = self.client.patch(self.post_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_delete_view_owner(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.post_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_post_delete_view_non_owner(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.post_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_like_post_authenticated(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(user=self.user2, post=self.post).exists())

    def test_like_post_unauthenticated(self):
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_like_own_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_like_post_already_liked(self):
        self.client.force_authenticate(user=self.user2)
        Like.objects.create(user=self.user2, post=self.post)
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unlike_post_authenticated(self):
        self.client.force_authenticate(user=self.user2)
        Like.objects.create(user=self.user2, post=self.post)
        response = self.client.delete(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Like.objects.filter(user=self.user2, post=self.post).exists())

    def test_unlike_post_not_liked(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
