from typing import Self

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class Subscription(models.Model):
    """
    Подписка пользователя на автора.
    Разовая оплата на выбранный период.
    """

    PERIOD_CHOICES = [
        (1, _("1 месяц")),
        (3, _("3 месяца")),
        (6, _("6 месяцев")),
        (9, _("9 месяцев")),
        (12, _("12 месяцев")),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscribers",
        limit_choices_to={"is_author": True},
    )
    period_months = models.PositiveSmallIntegerField(_("период в месяцах"), choices=PERIOD_CHOICES)
    price = models.DecimalField(
        _("цена"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    start_date = models.DateTimeField(_("дата начала"), auto_now_add=True)
    end_date = models.DateTimeField(_("дата окончания"))
    is_active = models.BooleanField(_("активна"), default=True)
    stripe_subscription_id = models.CharField(_("ID подписки в Stripe"), max_length=100, blank=True, null=True)
    auto_renew = models.BooleanField(_("автопродление"), default=True)

    class Meta:
        verbose_name = _("подписка")
        verbose_name_plural = _("подписки")
        unique_together = ["user", "author"]

    def __str__(self) -> str:
        return f"{self.user.phone_number} подписан на {self.author.phone_number} на {self.period_months} мес."
