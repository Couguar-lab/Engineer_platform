import json
from datetime import timedelta

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from notifications.models import Notification
from users.models import User

from .models import Subscription
from .stripe_utils import create_checkout_session


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session.get("metadata", {})

        # Проверяем, что это наше событие (от нашей сессии)
        user_id = metadata.get("user_id")
        author_id = metadata.get("author_id")
        period_months = metadata.get("period_months")

        if not all([user_id, author_id, period_months]):
            print("Webhook: тестовое событие без metadata — пропускаем")
            return HttpResponse(status=200)

        try:
            user = User.objects.get(id=user_id)
            author = User.objects.get(id=author_id)

            Subscription.objects.update_or_create(
                user=user,
                author=author,
                defaults={
                    "period_months": int(period_months),
                    "price": session["amount_total"] / 100,
                    "start_date": timezone.now(),
                    "end_date": timezone.now() + timedelta(days=int(period_months) * 30),
                    "is_active": True,
                    "stripe_subscription_id": session["subscription"],
                    "auto_renew": True,
                },
            )

            Notification.objects.create(
                user=user,
                message=f"Подписка на {author.phone_number} активирована на {period_months} месяцев!",
                is_read=False,
            )

            print("Webhook: подписка активирована для пользователя", user.phone_number)
        except User.DoesNotExist:
            print("Webhook: пользователь не найден", user_id)
            return HttpResponse(status=400)

    return HttpResponse(status=200)


@login_required
@require_POST
def create_subscription(request: HttpRequest, author_id: int, period: int) -> HttpResponse:
    """
    Создаёт Stripe Checkout сессию для подписки на автора.
    Редиректит пользователя на оплату.
    """
    author = get_object_or_404(User, id=author_id, is_author=True)

    if author == request.user:
        return redirect("post_list")  # Нельзя подписаться на себя

    session_data = create_checkout_session(
        user_id=request.user.id,
        author_id=author.id,
        period_months=period,
        request=request,
    )

    return redirect(session_data["url"])
