from typing import Self

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from users.models import User


class Notification(models.Model):
    """
    Уведомление пользователя (например, о новой платной записи от автора).
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField(_("сообщение"))
    is_read = models.BooleanField(_("прочитано"), default=False)
    created_at = models.DateTimeField(_("дата создания"), default=timezone.now)

    class Meta:
        verbose_name = _("уведомление")
        verbose_name_plural = _("уведомления")
        ordering = ["-created_at"]
        app_label = "notifications"

    def __str__(self) -> str:
        return f"Уведомление для {self.user.phone_number}: {self.message[:50]}..."
