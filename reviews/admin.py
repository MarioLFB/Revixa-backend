from django.contrib import admin
from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'framework_name', 'framework_version', 'author', 'created_at')
    search_fields = ('title', 'framework_name', 'author__username')
    list_filter = ('framework_name', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Review, ReviewAdmin)
