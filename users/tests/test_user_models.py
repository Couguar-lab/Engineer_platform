from django.test import TestCase

from users.models import User


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(phone_number="+79123456789")
        self.assertEqual(user.phone_number, "+79123456789")
        self.assertFalse(user.is_author)
        self.assertFalse(user.is_moderator)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(phone_number="+79267660693")
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_active)
