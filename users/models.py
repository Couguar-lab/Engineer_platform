from typing import Any, List

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager["User"]):
    """
    Менеджер для создания пользователей и суперпользователей по номеру телефона.
    """

    use_in_migrations = True

    def _create_user(
        self,
        phone_number: str,
        password: str | None,
        **extra_fields: Any,
    ) -> "User":
        """
        Внутренний метод создания пользователя.
        """
        if not phone_number:
            raise ValueError("Номер телефона обязателен")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        phone_number: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "User":
        """
        Создаёт обычного пользователя.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(
        self,
        phone_number: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "User":
        """
        Создаёт суперпользователя.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    """
    Пользователь платформы, регистрируется и аутентифицируется по номеру телефона.
    """

    username = None
    email = None

    phone_number = models.CharField(
        _("номер телефона"),
        max_length=20,
        unique=True,
        help_text=_("Обязательное поле. Номер в международном формате, например +79123456789"),
        error_messages={
            "unique": _("Пользователь с таким номером телефона уже существует."),
        },
    )

    is_author = models.BooleanField(
        _("автор"),
        default=False,
        help_text=_("Указывает, может ли пользователь публиковать записи."),
    )

    is_moderator = models.BooleanField(
        _("модератор"),
        default=False,
        help_text=_("Указывает, имеет ли пользователь права модератора."),
    )

    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD: str = "phone_number"
    REQUIRED_FIELDS: List[str] = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.phone_number

    class Meta:
        verbose_name = _("пользователь")
        verbose_name_plural = _("пользователи")
