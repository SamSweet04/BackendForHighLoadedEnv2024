from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.db import connection
from django.shortcuts import render, get_object_or_404
from .models import Post

@cache_page(60)
def post_list_view(request):
    #posts = Post.objects.all()
    #posts = Post.objects.prefetch_related('comments').all()
    #posts = Post.objects.select_related('author').prefetch_related('comments').all()
    posts = Post.objects.select_related('author').prefetch_related('comments__author').all()


    response = render(request, 'post_list.html', {'posts': posts})


    for query in connection.queries:
        print(query['sql'])

    return response

def post_detail_view(request, post_id):
    post = get_object_or_404(Post.objects.prefetch_related('comments__author'), id=post_id)


    cache_key = f'comments_count_{post_id}'
    comments_count = cache.get(cache_key)

    if comments_count is None:
        comments_count = post.comments.count()
        cache.set(cache_key, comments_count, 60)

    return render(request, 'post_detail.html', {'post': post, 'comments_count': comments_count})

