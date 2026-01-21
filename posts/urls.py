from django.urls import path

from .views import complain_post, post_create, post_detail, post_list

urlpatterns = [
    path("create/", post_create, name="post_create"),
    path("<int:post_id>/", post_detail, name="post_detail"),
    path("", post_list, name="post_list"),
    path("<int:post_id>/complain/", complain_post, name="complain_post"),
]
