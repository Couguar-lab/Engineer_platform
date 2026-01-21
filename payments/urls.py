from django.urls import path

from .views import create_subscription, stripe_webhook

urlpatterns = [
    path("subscribe/<int:author_id>/<int:period>/", create_subscription, name="create_subscription"),
    path("webhook/stripe/", stripe_webhook, name="stripe_webhook"),
]
