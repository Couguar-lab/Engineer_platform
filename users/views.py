import json

import firebase_admin
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials, initialize_app

from payments.models import Subscription
from themes.models import Theme

from .models import User

# Инициализация Firebase один раз при загрузке модуля
if not firebase_admin._apps:
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)


@require_http_methods(["GET", "POST"])
def login_view(request: HttpRequest) -> HttpResponse:
    """
    Страница входа по номеру телефона + отправка OTP через Firebase (клиентская сторона).
    """
    return render(request, "registration/login.html")


@require_http_methods(["GET", "POST"])
def otp_verify_view(request: HttpRequest) -> HttpResponse:
    """
    Проверка OTP-кода от Firebase и вход/регистрация пользователя.
    """
    if request.method == "POST" and request.headers.get("Content-Type") == "application/json":
        data = json.loads(request.body)
        id_token = data.get("id_token")
        if not id_token:
            return JsonResponse({"error": "No id_token"}, status=400)

        try:
            decoded = firebase_auth.verify_id_token(id_token)
            phone = decoded["phone_number"]
            user, _ = User.objects.get_or_create(phone_number=phone, defaults={"is_active": True})
            login(request, user)
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return render(request, "registration/otp_verify.html")


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
