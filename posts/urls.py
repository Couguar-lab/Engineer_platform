from django.urls import path, include

from posts.views import post_detail

urlpatterns = [
    path('<int:post_id>/', post_detail, name='post_detail'),
    path('posts/', include('posts.urls')),

]
