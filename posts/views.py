from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from posts.models import Post


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
        'periods': [(1, '1 месяц'), (3, '3 месяца'), (6, '6 месяцев'), (9, '9 месяцев'), (12, '12 месяцев')],
        'prices': {1: 500, 3: 1200, 6: 2000, 9: 3000, 12: 5000},  # пример цен
    }
    return render(request, 'posts/post_detail.html', context)