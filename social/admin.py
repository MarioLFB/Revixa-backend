from django.contrib import admin
from .models import Post, Like


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content', 'created_at', 'updated_at', 'review')
    search_fields = ('content', 'author__username')
    list_filter = ('created_at', 'updated_at', 'author')
    readonly_fields = ('created_at', 'updated_at')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created_at')
    search_fields = ('user__username', 'post__content')
    list_filter = ('created_at', 'user')
    readonly_fields = ('created_at',)


admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
