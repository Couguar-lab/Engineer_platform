from django.test import Client, TestCase
from django.urls import reverse

from themes.models import Theme
from users.models import User


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(phone_number="+79123456789")
        self.client.force_login(self.user)
        Theme.objects.create(user=self.user, theme="light")

    def test_profile_view_get(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")
        self.assertContains(response, "+79123456789")
