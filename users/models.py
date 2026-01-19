from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone number must be set")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    username = None  # отключаем username, так как регистрируемся по телефону
    email = None  # отключаем email

    phone_number = models.CharField(
        _("phone number"),
        max_length=20,
        unique=True,
        help_text=_("Required. Phone number in international format, e.g. +79123456789"),
        error_messages={
            "unique": _("A user with this phone number already exists."),
        },
    )

    is_author = models.BooleanField(
        _("is author"),
        default=False,
        help_text=_("Designates whether this user can publish posts."),
    )

    is_moderator = models.BooleanField(
        _("is moderator"),
        default=False,
        help_text=_("Designates whether this user has moderator privileges."),
    )

    # Отключаем ненужные поля из AbstractUser
    first_name = None
    last_name = None
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserManager()  # нужно будет создать менеджер ниже

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
