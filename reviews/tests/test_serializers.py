from django.test import TestCase
from django.contrib.auth.models import User
from reviews.models import Review
from reviews.serializers import ReviewSerializer

class ReviewSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123', email='testuser@example.com'
        )
        self.review = Review.objects.create(
            title='Test Review',
            content='This is a test review.',
            framework_name='Django',
            framework_version='3.2',
            author=self.user
        )

    def test_review_serializer_serialization(self):
        serializer = ReviewSerializer(self.review)
        data = serializer.data
        self.assertEqual(data['title'], 'Test Review')
        self.assertEqual(data['content'], 'This is a test review.')
        self.assertEqual(data['framework_name'], 'Django')
        self.assertEqual(data['framework_version'], '3.2')
        self.assertEqual(data['author'], 'testuser')
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
        self.assertEqual(data['posts'], [])

    def test_review_serializer_deserialization(self):
        data = {
            'title': 'New Review',
            'content': 'This is a new review.',
            'framework_name': 'Flask',
            'framework_version': '2.0',
        }
        serializer = ReviewSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        review = serializer.save(author=self.user)
        self.assertEqual(review.title, data['title'])
        self.assertEqual(review.content, data['content'])
        self.assertEqual(review.framework_name, data['framework_name'])
        self.assertEqual(review.framework_version, data['framework_version'])
        self.assertEqual(review.author, self.user)
