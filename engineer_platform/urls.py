from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import contacts
from payments.views import create_subscription, stripe_webhook

urlpatterns = [
    path("admin/", admin.site.urls),
    # Посты
    path("", include("posts.urls")),
    # Авторизация и профиль
    path("", include("users.urls")),
    # Уведомления
    path("notifications/", include("notifications.urls")),
    # Подписка
    path("subscribe/<int:author_id>/<int:period>/", create_subscription, name="create_subscription"),
    path("payments/", include("payments.urls")),
    # Webhook Stripe
    path("webhook/stripe/", stripe_webhook, name="stripe_webhook"),
    # Контакты
    path("contacts/", contacts, name="contacts"),
]

# Поддержка media в debug-режиме
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
