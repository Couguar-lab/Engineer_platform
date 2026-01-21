from django.urls import path

from .views import mark_notification_read, notification_list

urlpatterns = [
    path("", notification_list, name="notification_list"),
    path("<int:notification_id>/read/", mark_notification_read, name="mark_notification_read"),
]
