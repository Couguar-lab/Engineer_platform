from django.contrib import admin
from .models import Post, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Админка для тегов записей.
    """
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Админка для записей (постов).
    """
    list_display = ('title', 'author', 'is_paid', 'created_at', 'views', 'likes')
    list_filter = ('is_paid', 'tags', 'author')
    search_fields = ('title', 'content', 'author__phone_number')
    date_hierarchy = 'created_at'
    readonly_fields = ('views', 'likes', 'created_at')
    list_select_related = ('author',)