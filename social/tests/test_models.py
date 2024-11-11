from django.test import TestCase
from django.contrib.auth.models import User
from reviews.models import Review
from social.models import Post, Like

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
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

    def test_post_creation(self):
        self.assertEqual(self.post.content, 'This is a test post.')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.review, self.review)
        self.assertIsNotNone(self.post.created_at)
        self.assertIsNotNone(self.post.updated_at)

    def test_post_str_method(self):
        expected_str = f"Post by {self.user.username}"
        self.assertEqual(str(self.post), expected_str)

class LikeModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2', password='testpass123'
        )
        self.post = Post.objects.create(
            content='This is another test post.',
            author=self.user1
        )
        self.like = Like.objects.create(
            user=self.user2,
            post=self.post
        )

    def test_like_creation(self):
        self.assertEqual(self.like.user, self.user2)
        self.assertEqual(self.like.post, self.post)
        self.assertIsNotNone(self.like.created_at)

    def test_like_str_method(self):
        expected_str = f"{self.user2.username} liked {self.post.id}"
        self.assertEqual(str(self.like), expected_str)

    def test_like_unique_together(self):
        with self.assertRaises(Exception):
            Like.objects.create(user=self.user2, post=self.post)
