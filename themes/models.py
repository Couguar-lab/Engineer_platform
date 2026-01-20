from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class Theme(models.Model):
    THEME_CHOICES = [
        ("light", _("Light")),
        ("dark", _("Dark")),
        ("neon", _("Neon")),
        ("earth", _("Earth tones")),
        ("warm", _("Warm minimal")),
        ("high-contrast", _("High contrast")),
        ("sepia", _("Sepia/Retro")),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="theme")
    theme = models.CharField(_("theme"), max_length=20, choices=THEME_CHOICES, default="light")

    class Meta:
        verbose_name = _("theme")
        verbose_name_plural = _("themes")

    def __str__(self):
        return f"{self.user.phone_number}'s theme: {self.theme}"
