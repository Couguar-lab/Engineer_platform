from django.urls import path, include

from posts.views import post_detail, post_list

urlpatterns = [
    path('<int:post_id>/', post_detail, name='post_detail'),
    path('', post_list, name='post_list'),

]
