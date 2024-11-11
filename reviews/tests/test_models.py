from django.test import TestCase
from django.contrib.auth.models import User
from reviews.models import Review

class ReviewModelTest(TestCase):
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

    def test_review_creation(self):
        self.assertEqual(self.review.title, 'Test Review')
        self.assertEqual(self.review.content, 'This is a test review.')
        self.assertEqual(self.review.framework_name, 'Django')
        self.assertEqual(self.review.framework_version, '3.2')
        self.assertEqual(self.review.author, self.user)
        self.assertIsNotNone(self.review.created_at)
        self.assertIsNotNone(self.review.updated_at)

    def test_review_str_method(self):
        expected_str = f"Review: {self.review.title} by {self.user.username}"
        self.assertEqual(str(self.review), expected_str)
