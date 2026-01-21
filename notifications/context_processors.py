from .models import Notification


def notifications_count(request):
    """
    Контекст-процессор для счётчика непрочитанных уведомлений.
    Добавляет 'unread_notifications' в каждый шаблон.
    """
    if request.user.is_authenticated:
        return {"unread_notifications": Notification.objects.filter(user=request.user, is_read=False).count()}
    return {"unread_notifications": 0}
