from typing import Any, Dict

import stripe
from django.conf import settings
from django.http import HttpRequest
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY


PRICE_MAP = {
    1: "price_1SrjKeDNYXEsSHzUE5ADzexq",
    3: "price_1SrjOfDNYXEsSHzU7hbTGkEg",
    6: "price_1SrjOfDNYXEsSHzU3LovZiVP",
    9: "price_1SrjOfDNYXEsSHzUv55DAnDk",
    12: "price_1SrjOfDNYXEsSHzUi5gMlMeo",
}


def create_checkout_session(
    user_id: int,
    author_id: int,
    period_months: int,
    request: HttpRequest,
) -> Dict[str, Any]:
    """
    Создаёт Stripe Checkout сессию для подписки на автора.
    """
    price_id = PRICE_MAP.get(period_months)
    if not price_id:
        raise ValueError(f"Нет цены для периода {period_months} месяцев")

    success_url = request.build_absolute_uri(reverse("post_list")) + "?session_id={CHECKOUT_SESSION_ID}"
    cancel_url = request.build_absolute_uri(reverse("post_list"))

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="subscription",
        success_url=success_url,
        cancel_url=cancel_url,
        client_reference_id=f"{user_id}_{author_id}_{period_months}",
        metadata={
            "user_id": str(user_id),
            "author_id": str(author_id),
            "period_months": str(period_months),
        },
    )

    return {"id": session.id, "url": session.url}
