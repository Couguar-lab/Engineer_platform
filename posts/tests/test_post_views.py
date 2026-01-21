from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Post
from users.models import User


class PostCreateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = get_user_model().objects.create_user(phone_number="+79991234567", is_author=True)
        self.client.force_login(self.author)

    def test_post_create_get(self):
        response = self.client.get(reverse("post_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_create.html")
        self.assertIsInstance(response.context["form"], PostForm)

    def test_post_create_post_valid(self):
        data = {
            "title": "Новый пост",
            "content": "Содержимое нового поста",
            "is_paid": False,
        }
        response = self.client.post(reverse("post_create"), data)
        self.assertEqual(response.status_code, 302)  # редирект на detail
        self.assertTrue(Post.objects.filter(title="Новый пост").exists())

    def test_post_create_not_author(self):
        non_author = get_user_model().objects.create_user(phone_number="+79123456789")
        self.client.force_login(non_author)
        response = self.client.get(reverse("post_create"))
        self.assertEqual(response.status_code, 302)  # редирект на список
        self.assertEqual(response.url, reverse("post_list"))


class PostViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(phone_number="+79991234567", is_author=True)
        self.post = Post.objects.create(author=self.author, title="Тестовый пост", content="Текст поста", is_paid=False)

    def test_post_list(self):
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_list.html")
        self.assertContains(response, "Тестовый пост")

    def test_post_detail(self):
        response = self.client.get(reverse("post_detail", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_detail.html")
        self.assertContains(response, "Тестовый пост")

    def test_post_create_not_author(self):
        user = User.objects.create_user(phone_number="+79123456789")
        self.client.force_login(user)
        response = self.client.get(reverse("post_create"))
        self.assertEqual(response.status_code, 302)  # редирект
        self.assertEqual(response.url, reverse("post_list"))
