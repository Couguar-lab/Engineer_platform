from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Complaint, Post, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Админка для тегов записей.
    """

    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Админка для записей (постов).
    """

    list_display = ("title", "author", "is_paid", "created_at", "views", "likes")
    list_filter = ("is_paid", "tags", "author")
    search_fields = ("title", "content", "author__phone_number")
    date_hierarchy = "created_at"
    readonly_fields = ("views", "likes", "created_at")
    list_select_related = ("author",)

    def complaint_count(self, obj):
        return obj.complaints.count()

    complaint_count.short_description = "Жалоб"


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("user", "post_link", "reason_short", "created_at", "resolved")
    list_filter = ("resolved", "created_at")
    search_fields = ("user__phone_number", "post__title", "reason")
    list_select_related = ("user", "post")
    actions = ["mark_resolved", "mark_unresolved"]

    def post_link(self, obj):
        return format_html(
            '<a href="{}">{}</a>', reverse("admin:posts_post_change", args=[obj.post.id]), obj.post.title
        )

    post_link.short_description = "Пост"

    def reason_short(self, obj):
        return obj.reason[:50] + "..." if len(obj.reason) > 50 else obj.reason

    reason_short.short_description = "Причина"

    def mark_resolved(self, request, queryset):
        queryset.update(resolved=True)
        self.message_user(request, "Выбранные жалобы отмечены как решённые.")

    mark_resolved.short_description = "Отметить как решённые"

    def mark_unresolved(self, request, queryset):
        queryset.update(resolved=False)
        self.message_user(request, "Выбранные жалобы отмечены как нерешённые.")

    mark_unresolved.short_description = "Отметить как нерешённые"
