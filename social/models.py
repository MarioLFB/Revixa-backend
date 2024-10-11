from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """
    Model representing a post in the social network.
    """
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return f"Post by {self.author.username}"