from typing import Self

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from payments.models import Subscription
from users.models import User


class Tag(models.Model):
    """
    Тег для классификации записей.
    """

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = _("тег")
        verbose_name_plural = _("теги")
        app_label = "posts"

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    """
    Запись (пост) пользователя.
    Может быть бесплатной или платной.
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(_("заголовок"), max_length=200)
    content = models.TextField(_("содержание"))
    is_paid = models.BooleanField(_("платная"), default=False)
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    youtube_link = models.URLField(_("ссылка на YouTube"), blank=True, null=True)
    images = models.ImageField(
        _("изображения"),
        upload_to="posts/images/",
        blank=True,
        null=True,
    )
    views = models.PositiveIntegerField(_("просмотры"), default=0)
    likes = models.PositiveIntegerField(_("лайки"), default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("запись")
        verbose_name_plural = _("записи")
        ordering = ["-created_at"]
        app_label = "posts"

    def __str__(self) -> str:
        return f"{self.title} от {self.author.phone_number}"

    def can_view(self, user: User) -> bool:
        """
        Проверяет, может ли пользователь просмотреть запись.
        Бесплатные — всем, платные — только подписчикам автора с активной подпиской.
        """
        if not self.is_paid:
            return True
        if user is None:
            return False
        if not user.is_authenticated:
            return False
        return Subscription.objects.filter(
            user=user, author=self.author, is_active=True, end_date__gte=timezone.now()
        ).exists()


class Complaint(models.Model):
    """
    Жалоба пользователя на пост.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="complaints")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="complaints")
    reason = models.TextField(_("причина жалобы"))
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(_("решено"), default=False)
    moderator_note = models.TextField(_("заметка модератора"), blank=True)

    class Meta:
        verbose_name = _("жалоба")
        verbose_name_plural = _("жалобы")
        unique_together = ["user", "post"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Жалоба от {self.user.phone_number} на пост '{self.post.title}'"
