from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
import json
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .stripe_utils import create_checkout_session
from users.models import User


@csrf_exempt
def stripe_webhook(request):
    """
    Webhook от Stripe для обработки событий оплаты.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session['metadata']

        user_id = metadata['user_id']
        author_id = metadata['author_id']
        period_months = int(metadata['period_months'])

        # Активируем подписку
        from users.models import User
        from .models import Subscription

        user = User.objects.get(id=user_id)
        author = User.objects.get(id=author_id)

        Subscription.objects.update_or_create(
            user=user,
            author=author,
            defaults={
                'period_months': period_months,
                'price': session['amount_total'] / 100,  # в долларах
                'start_date': timezone.now(),
                'end_date': timezone.now() + timezone.timedelta(days=period_months * 30),
                'is_active': True,
                'stripe_subscription_id': session['subscription'],
                'auto_renew': True,
            }
        )

        # Можно отправить уведомление
        from notifications.models import Notification
        Notification.objects.create(
            user=user,
            message=f"Подписка на {author.phone_number} активирована на {period_months} месяцев!",
            is_read=False
        )

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
        return redirect('post_list')  # Нельзя подписаться на себя

    session_data = create_checkout_session(
        user_id=request.user.id,
        author_id=author.id,
        period_months=period,
        request=request,
    )

    return redirect(session_data['url'])