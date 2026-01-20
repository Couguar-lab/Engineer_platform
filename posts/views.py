from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from posts.models import Post


@login_required
def post_detail(request, post_id):
    """
    Детальная страница поста с проверкой доступа.
    """
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})