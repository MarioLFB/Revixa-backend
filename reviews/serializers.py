from rest_framework import serializers
from .models import Review
from social.serializers import PostSerializer

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'title', 'content', 'framework_name', 'framework_version', 'author', 'created_at', 'updated_at', 'posts']