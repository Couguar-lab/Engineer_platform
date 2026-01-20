from django.urls import path

from posts.views import post_detail

urlpatterns = [
    path('<int:post_id>/', post_detail, name='post_detail'),

]
