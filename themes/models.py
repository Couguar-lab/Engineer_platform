from typing import Self

from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class Theme(models.Model):
    """
    Настройка цветовой темы интерфейса пользователя.
    """

    THEME_CHOICES = [
        ("light", _("Светлая")),
        ("dark", _("Тёмная")),
        ("neon", _("Неон")),
        ("earth", _("Земляные тона")),
        ("warm", _("Тёплый минимализм")),
        ("high-contrast", _("Высокий контраст")),
        ("sepia", _("Сепия / Ретро")),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="theme")
    theme = models.CharField(_("тема"), max_length=20, choices=THEME_CHOICES, default="light")

    class Meta:
        verbose_name = _("тема")
        verbose_name_plural = _("темы")
        app_label = "themes"

    def __str__(self) -> str:
        return f"Тема пользователя {self.user.phone_number}: {self.theme}"
