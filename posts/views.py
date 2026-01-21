from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from notifications.models import Notification
from payments.models import Subscription

from .forms import PostForm
from .models import Complaint, Post, Tag


def post_list(request: HttpRequest) -> HttpResponse:
    """
    Главная страница — список всех постов с базовыми фильтрами.
    """
    posts = Post.objects.all().order_by("-created_at")

    # Простые GET-фильтры (можно расширить django-filter позже)
    q = request.GET.get("q")
    if q:
        posts = posts.filter(title__icontains=q) | posts.filter(content__icontains=q)

    free_only = request.GET.get("free") == "1"
    if free_only:
        posts = posts.filter(is_paid=False)

    for post in posts:
        post.has_access = post.can_view(request.user)

    context = {
        "posts": posts,
        "periods": [(1, "1 месяц"), (3, "3 месяца"), (6, "6 месяцев"), (9, "9 месяцев"), (12, "12 месяцев")],
        "prices": {1: 500, 3: 1200, 6: 2000, 9: 3000, 12: 5000},
        "q": q,
        "free_only": free_only,
    }
    return render(request, "posts/post_list.html", context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """
    Детальная страница поста.
    """
    post = get_object_or_404(Post, id=post_id)
    has_access = post.can_view(request.user)

    # Увеличиваем просмотры только при реальном доступе
    if has_access:
        post.views += 1
        post.save(update_fields=["views"])

    context = {
        "post": post,
        "has_access": has_access,
        "periods": [(1, "1 месяц"), (3, "3 месяца"), (6, "6 месяцев"), (9, "9 месяцев"), (12, "12 месяцев")],
        "prices": {1: 500, 3: 1200, 6: 2000, 9: 3000, 12: 5000},
    }
    return render(request, "posts/post_detail.html", context)


@login_required
def post_create(request: HttpRequest) -> HttpResponse:
    """
    Создание новой записи (только для авторов).
    """
    if not request.user.is_author:
        messages.error(request, "Только авторы могут создавать записи.")
        return redirect("post_list")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # сохраняем теги

            # Если пост платный — уведомляем всех активных подписчиков
            if post.is_paid:
                subscribers = Subscription.objects.filter(
                    author=request.user, is_active=True, end_date__gte=timezone.now()
                ).select_related("user")

                for sub in subscribers:
                    Notification.objects.create(
                        user=sub.user,
                        message=f"Новый платный пост от {request.user.phone_number}: «{post.title}»",
                        is_read=False,
                    )

            messages.success(request, "Запись успешно создана!")
            return redirect("post_detail", post.id)
    else:
        form = PostForm()

    return render(request, "posts/post_create.html", {"form": form})


@login_required
def complain_post(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        reason = request.POST.get("reason")
        if reason and len(reason.strip()) > 10:  # минимальная длина
            Complaint.objects.get_or_create(user=request.user, post=post, defaults={"reason": reason})
            messages.success(request, "Жалоба отправлена модераторам. Спасибо!")
        else:
            messages.error(request, "Укажите подробную причину жалобы (минимум 10 символов).")

    return redirect("post_detail", post_id)
