from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .models import Notification


@login_required
def notification_list(request: HttpRequest) -> HttpResponse:
    """
    Список уведомлений пользователя.
    """
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "notifications/notification_list.html", {"notifications": notifications})


@login_required
def mark_notification_read(request: HttpRequest, notification_id: int) -> HttpResponse:
    """
    Отметить уведомление как прочитанное.
    """
    notification = Notification.objects.filter(id=notification_id, user=request.user).first()
    if notification:
        notification.is_read = True
        notification.save()
    return redirect("notification_list")
