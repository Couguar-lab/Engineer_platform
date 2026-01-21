from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from posts.models import Post


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    has_access = post.can_view(request.user)
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'has_access': has_access
    })

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/post_list.html', {'posts': posts})