from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import Post, PostForm, CommentForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator


def index(request):
    return HttpResponse("Hello, Blog!")


def post_list(request):
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', id=post.id)
    return render(request, 'blog/post_detail.html', {'post': post, 'comment_form': comment_form})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        return redirect('post_list')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        return redirect('post_list')
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})




