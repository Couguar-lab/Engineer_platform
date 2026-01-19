from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Поля, которые показываем в списке пользователей
    list_display = ('phone_number', 'is_author', 'is_moderator', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('is_author', 'is_moderator', 'is_staff', 'is_superuser')
    search_fields = ('phone_number',)

    # Поля для формы создания/редактирования пользователя
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_author', 'is_moderator')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Поля только для создания нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2', 'is_author', 'is_moderator'),
        }),
    )

    # Отключаем поля, которые не нужны
    ordering = ('phone_number',)
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)