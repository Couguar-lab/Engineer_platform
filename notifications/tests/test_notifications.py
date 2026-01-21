from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from notifications.models import Notification
from payments.models import Subscription
from posts.models import Post
from users.models import User


class NotificationTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(phone_number="+79991234567", is_author=True)
        self.subscriber = User.objects.create_user(phone_number="+79123456789")
        Subscription.objects.create(
            user=self.subscriber,
            author=self.author,
            period_months=1,
            price=500,
            end_date=timezone.now() + timezone.timedelta(days=30),
            is_active=True,
        )

    def test_notification_created_on_paid_post(self):
        self.client.force_login(self.author)

        # Создаём платный пост через view
        data = {
            "title": "Платный пост для теста",
            "content": "Текст",
            "is_paid": True,
        }
        self.client.post(reverse("post_create"), data)

        # Проверяем, что уведомление появилось
        notification = Notification.objects.filter(user=self.subscriber).first()
        assert notification is not None
        assert "Новый платный пост" in notification.message
        assert notification.is_read is False
