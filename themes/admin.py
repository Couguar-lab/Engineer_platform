from django.contrib import admin
from .models import Theme


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    """
    Админка для настроек тем пользователей.
    """
    list_display = ('user', 'theme')
    search_fields = ('user__phone_number',)
    list_select_related = ('user',)