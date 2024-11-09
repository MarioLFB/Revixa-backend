from django.urls import path
from .views import PostListCreateView, PostDetailView, LikePostView

urlpatterns = [
    path(
        'reviews/<int:review_id>/posts/',
        PostListCreateView.as_view(),
        name='review-post-list-create'
    ),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path(
        'posts/<int:post_id>/like/',
        LikePostView.as_view(),
        name='like-post'
    ),
]
