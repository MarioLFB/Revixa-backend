from rest_framework import serializers
from .models import Post, Like
from reviews.models import Review

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    author = serializers.ReadOnlyField(source='author.username')
    liked_by = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at', 'updated_at', 'likes_count', 'liked_by', 'is_liked', 'review']

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_liked_by(self, obj):
        return [like.user.username for like in obj.likes.all()]
    
    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']