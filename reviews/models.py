from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    """
    Model for storing reviews of frameworks
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    framework_name = models.CharField(max_length=255)
    framework_version = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE
)

    def __str__(self):
        return (
            f"Review: {self.title} by {self.author.username}"
        )
