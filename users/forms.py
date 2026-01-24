from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class UserRegistrationForm(UserCreationForm):
    """
    Форма регистрации пользователя по номеру телефона.
    """

    phone_number = forms.CharField(
        max_length=20,
        required=True,
        label="Номер телефона",
        help_text="Введите номер в формате +79123456789",
    )

    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Пароль должен быть минимум 8 символов, содержать буквы верхнего и нижнего регистра, цифры и спецсимволы (@$!%*#?&).",
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Повторите пароль для подтверждения.",
    )

    class Meta:
        model = User
        fields = ("phone_number", "password1", "password2")

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Пользователь с таким номером телефона уже существует.")
        return phone_number


class UserLoginForm(AuthenticationForm):
    """
    Форма входа по номеру телефона и паролю.
    """

    username = forms.CharField(
        max_length=20,
        required=True,
        label="Номер телефона",
        help_text="Введите номер в формате +79123456789",
    )

    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput,
    )

    error_messages = {
        "invalid_login": "Неверный логин или пароль.",
        "inactive": "Этот аккаунт деактивирован.",
    }

    class Meta:
        model = User
        fields = ("username", "password")