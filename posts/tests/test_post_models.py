from django.test import TestCase
from django.utils import timezone

from payments.models import Subscription
from posts.models import Post, Tag
from users.models import User


class PostModelTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(phone_number="+79991234567", is_author=True)
        self.user = User.objects.create_user(phone_number="+79123456789")
        self.tag = Tag.objects.create(name="Тестовый тег")

        self.post_free = Post.objects.create(
            author=self.author, title="Бесплатный пост", content="Текст", is_paid=False
        )
        self.post_free.tags.add(self.tag)

        self.post_paid = Post.objects.create(author=self.author, title="Платный пост", content="Текст", is_paid=True)
        self.post_paid.tags.add(self.tag)

    def test_can_view_free_post(self):
        self.assertTrue(self.post_free.can_view(self.user))
        self.assertTrue(self.post_free.can_view(None))

    def test_can_view_paid_post(self):
        self.assertFalse(self.post_paid.can_view(None))
        self.assertFalse(self.post_paid.can_view(self.user))

    def test_can_view_paid_post_with_subscription(self):
        Subscription.objects.create(
            user=self.user,
            author=self.author,
            period_months=1,
            price=500,
            end_date=timezone.now() + timezone.timedelta(days=30),
            is_active=True,
        )
        self.assertTrue(self.post_paid.can_view(self.user))
