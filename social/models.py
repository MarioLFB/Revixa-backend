from django.db import models
from django.contrib.auth.models import User
from reviews.models import Review


class Post(models.Model):
    """
    Model representing a post in the social network.
    """
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review,
        related_name='posts',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Post by {self.author.username}"


class Like(models.Model):
    """
    Model representing a like in a post.
    """
    user = models.ForeignKey(
        User,
        related_name='likes',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        related_name='likes',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"