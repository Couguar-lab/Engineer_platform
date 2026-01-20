import stripe
from django.conf import settings

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(
    user: User,
    author: User,
    period_months: int,
    success_url: str,
    cancel_url: str,
) -> stripe.checkout.Session:
    """
    Создаёт Stripe Checkout сессию для подписки на автора.
    """
    # Находим price ID по периоду
    price_map = {
        1: "price_1SrjKeDNYXEsSHzUE5ADzexq",
        3: "price_1SrjOfDNYXEsSHzU7hbTGkEg",
        6: "price_1SrjOfDNYXEsSHzU3LovZiVP",
        9: "price_1SrjOfDNYXEsSHzUv55DAnDk",
        12: "price_1SrjOfDNYXEsSHzUi5gMlMeo",
    }

    price_id = price_map.get(period_months)
    if not price_id:
        raise ValueError("Неверный период подписки")

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url=success_url,
        cancel_url=cancel_url,
        client_reference_id=f"{user.id}_{author.id}_{period_months}",
        metadata={
            'user_id': user.id,
            'author_id': author.id,
            'period_months': period_months,
        }
    )

    return session