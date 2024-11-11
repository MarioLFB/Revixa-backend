from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from reviews.models import Review
from social.models import Post, Like
from social.serializers import PostSerializer, LikeSerializer

class PostSerializerTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
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

    def test_post_serializer_serialization(self):
        request = self.factory.get('/')
        request.user = self.user
        serializer = PostSerializer(self.post, context={'request': request})
        data = serializer.data
        self.assertEqual(data['content'], 'This is a test post.')
        self.assertEqual(data['author'], 'testuser')
        self.assertEqual(data['likes_count'], 0)
        self.assertEqual(data['liked_by'], [])
        self.assertFalse(data['is_liked'])
        self.assertEqual(data['review'], self.review.id)

    def test_post_serializer_deserialization(self):
        data = {
            'content': 'New test post.',
            'review': self.review.id
        }
        serializer = PostSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        post = serializer.save(author=self.user)
        self.assertEqual(post.content, data['content'])
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.review, self.review)

class LikeSerializerTest(TestCase):
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

    def test_like_serializer_serialization(self):
        serializer = LikeSerializer(self.like)
        data = serializer.data
        self.assertEqual(data['user'], self.user2.id)
        self.assertEqual(data['post'], self.post.id)
        self.assertIsNotNone(data['created_at'])
