# payments/views.py (обновлённый)
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


stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
@require_POST
def create_subscription(request: HttpRequest, author_id: int, period: int) -> HttpResponse:
    """
    Создаёт Stripe Checkout сессию для подписки на автора.
    """
    author = get_object_or_404(User, id=author_id, is_author=True)

    if author == request.user:
        return redirect("post_list")

    session_data = create_checkout_session(
        user_id=request.user.id,
        author_id=author.id,
        period_months=period,
        request=request,
    )

    return redirect(session_data["url"])


@csrf_exempt
def stripe_webhook(request: HttpRequest) -> HttpResponse:
    """
    Webhook от Stripe для обработки успешной оплаты подписки.
    """
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


def subscription_info(request: HttpRequest) -> HttpResponse:
    """
    Отображает страницу с информацией о подписке и актуальными тарифами из Stripe.
    Запрашивает активные продукты и их цены (recurring) через Stripe API.
    """
    try:
        # Получаем все активные продукты
        products = stripe.Product.list(active=True)

        plans = []
        for product in products.auto_paging_iter():
            # Получаем все активные recurring цены для этого продукта
            prices = stripe.Price.list(
                product=product.id,
                active=True,
                type="recurring"
            )
            for price in prices.auto_paging_iter():
                plans.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'price_id': price.id,
                    'amount': price.unit_amount / 100,  # в рублях/долларах и т.д.
                    'currency': price.currency.upper(),
                    'interval': price.recurring.interval,  # month, year
                    'interval_count': price.recurring.interval_count,
                    'description': product.description or "Подписка на эксклюзивный контент",
                })

        # Сортируем по цене (по возрастанию)
        plans.sort(key=lambda x: x['amount'])

    except stripe.error.StripeError as e:
        # Если ошибка — показываем пустой список, но не падаем
        plans = []
        print(f"Stripe API error in subscription_info: {e}")

    context = {
        'title': 'Подписка',
        'plans': plans,
        'has_plans': len(plans) > 0,
    }

    return render(request, 'payments/subscription_info.html', context)