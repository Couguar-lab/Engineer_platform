from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Админка для уведомлений пользователей.
    """
    list_display = ('user', 'message_short', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('user__phone_number', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    list_select_related = ('user',)

    def message_short(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_short.short_description = "Сообщение"