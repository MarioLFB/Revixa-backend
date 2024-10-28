from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer
from reviews.models import Review


class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        if review_id:
            return Post.objects.filter(review_id=review_id)
        return Post.objects.filter(review__isnull=True)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        if review_id:
            review = get_object_or_404(Review, id=review_id)
            serializer.save(author=self.request.user, review=review)
        else:
            serializer.save(author=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}        


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        post = super().get_object()
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if post.author != self.request.user:
                raise permissions.PermissionDenied("You are not allowed to modify this comment.")
        return post
    
    def get_serializer_context(self):
        return {'request': self.request}


class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        if post.author == request.user:
            return Response({"detail": "You cannot like your own post."}, status=status.HTTP_403_FORBIDDEN)
        
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        
        like = Like.objects.create(user=request.user, post=post)
        return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({"detail": "You didn't like this post."}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)