from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Кастомная админка для модели User.
    Показывает номер телефона, роли, даты и позволяет быстро фильтровать/искать.
    """

    list_display = (
        "phone_number",
        "is_author",
        "is_moderator",
        "is_staff",
        "is_superuser",
        "date_joined",
        "is_active",
    )
    list_filter = (
        "is_author",
        "is_moderator",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    search_fields = ("phone_number",)
    ordering = ("phone_number",)
    readonly_fields = ("date_joined", "last_login")

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Роли и права", {"fields": ("is_active", "is_staff", "is_superuser", "is_author", "is_moderator")}),
        (
            "Даты",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "password1",
                    "password2",
                    "is_author",
                    "is_moderator",
                ),
            },
        ),
    )

    # Отключаем поля, которые не нужны в нашей модели
    exclude = ("username", "email", "first_name", "last_name")

    # Отображаем поле в списке, даже если оно None
    def get_list_display(self, request):
        return super().get_list_display(request)
