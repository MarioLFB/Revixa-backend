from rest_framework import serializers
from .models import Post, Like

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    author = serializers.ReadOnlyField(source='author.username')
    liked_by = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at', 'updated_at', 'likes_count', 'liked_by']

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_liked_by(self, obj):
        return [like.user.username for like in obj.likes.all()]

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']