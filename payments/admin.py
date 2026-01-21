from django.contrib import admin
from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Админка для подписок пользователей на авторов.
    """
    list_display = ('user', 'author', 'period_months', 'price', 'is_active', 'start_date', 'end_date')
    list_filter = ('is_active', 'period_months', 'auto_renew')
    search_fields = ('user__phone_number', 'author__phone_number')
    date_hierarchy = 'start_date'
    list_select_related = ('user', 'author')