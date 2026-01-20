from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from posts.models import Post
from users.models import User


class Subscription(models.Model):
    PERIOD_CHOICES = [
        (1, _("1 month")),
        (3, _("3 months")),
        (6, _("6 months")),
        (9, _("9 months")),
        (12, _("12 months")),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscribers", limit_choices_to={"is_author": True}
    )
    period_months = models.PositiveSmallIntegerField(_("period in months"), choices=PERIOD_CHOICES)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    start_date = models.DateTimeField(_("start date"), auto_now_add=True)
    end_date = models.DateTimeField(_("end date"))
    is_active = models.BooleanField(_("is active"), default=True)
    stripe_subscription_id = models.CharField(_("Stripe subscription ID"), max_length=100, blank=True, null=True)
    auto_renew = models.BooleanField(_("auto renew"), default=True)

    class Meta:
        verbose_name = _("subscription")
        verbose_name_plural = _("subscriptions")
        unique_together = ["user", "author"]

    def __str__(self):
        return f"{self.user.phone_number} subscribed to {self.author.phone_number} for {self.period_months} months"
