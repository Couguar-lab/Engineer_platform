import json
import sys

import firebase_admin
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials, initialize_app

from payments.models import Subscription
from themes.models import Theme

from .forms import UserLoginForm, UserRegistrationForm
from .models import User

firebase_app = None
firebase_auth_module = None

def init_firebase():
    global firebase_app, firebase_auth_module
    if firebase_app is None:
        # Пропускаем в тестах и в DEBUG-режиме без реального использования
        if 'test' in sys.argv or settings.DEBUG and not 'runserver' in sys.argv:
            from unittest.mock import MagicMock
            firebase_auth_module = MagicMock()
            firebase_app = MagicMock()
            return firebase_auth_module

        # Реальная инициализация
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        firebase_app = firebase_admin.initialize_app(cred)
        firebase_auth_module = firebase_auth
    return firebase_auth_module

# Инициализация Firebase один раз при загрузке модуля
# if not firebase_admin._apps:
#     cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
#     firebase_admin.initialize_app(cred)


@require_http_methods(["GET", "POST"])
def login_view(request: HttpRequest) -> HttpResponse:
    """
    Страница входа по номеру телефона и паролю.
    """
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                messages.success(request, "Вход выполнен успешно!")
                return redirect("post_list")
            else:
                messages.error(request, "Неверный логин или пароль")
        else:
            messages.error(request, "Неверный логин или пароль")
    else:
        form = UserLoginForm()

    return render(request, "registration/login.html", {"form": form})


@require_http_methods(["GET", "POST"])
def register_view(request: HttpRequest) -> HttpResponse:
    """
    Страница регистрации: телефон + пароль + подтверждение.
    Создаёт пользователя с is_author=True.
    """
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_author = True  # Делаем пользователя автором
            user.save()
            messages.success(request, "Регистрация успешна! Теперь вы можете войти.")
            return redirect("login")
    else:
        form = UserRegistrationForm()

    return render(request, "users/register.html", {"form": form})


def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Выход пользователя.
    """
    logout(request)
    messages.info(request, "Вы вышли из аккаунта")
    return redirect("post_list")


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """
    Профиль пользователя: подписки, остаток времени, выбор темы.
    """
    subscriptions = Subscription.objects.filter(user=request.user).select_related("author")
    theme = Theme.objects.get_or_create(user=request.user)[0]

    if request.method == "POST":
        new_theme = request.POST.get("theme")
        if new_theme in dict(Theme.THEME_CHOICES):
            # Проверка: премиум-темы только для платных пользователей (с активной подпиской)
            has_active_subscription = subscriptions.filter(is_active=True, end_date__gte=timezone.now()).exists()
            free_themes = ["light", "dark"]
            if new_theme not in free_themes and not has_active_subscription:
                messages.error(request, "Премиум-темы доступны только для пользователей с активной подпиской.")
            else:
                theme.theme = new_theme
                theme.save()
                messages.success(request, "Тема успешно изменена!")
        return redirect("profile")

    context = {
        "subscriptions": subscriptions,
        "theme": theme,
        "has_active_subscription": subscriptions.filter(is_active=True, end_date__gte=timezone.now()).exists(),
    }
    return render(request, "users/profile.html", context)