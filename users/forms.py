from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegistrationForm(UserCreationForm):
    """
    Форма регистрации пользователя по номеру телефона.
    """

    phone_number = forms.CharField(
        max_length=20,
        required=True,
        label=_("Номер телефона"),
        help_text=_("Введите номер в формате +79123456789"),
    )

    class Meta:
        model = User
        fields = ("phone_number", "password1", "password2")

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(_("Пользователь с таким номером телефона уже существует."))
        return phone_number
