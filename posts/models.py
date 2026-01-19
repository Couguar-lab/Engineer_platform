from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(_("title"), max_length=200)
    content = models.TextField(_("content"))
    is_paid = models.BooleanField(_("is paid"), default=False)
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    youtube_link = models.URLField(_("YouTube link"), blank=True, null=True)
    views = models.PositiveIntegerField(_("views"), default=0)
    likes = models.PositiveIntegerField(_("likes"), default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} by {self.author.phone_number}"