from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostForm
from .models import Post


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'community/post_list.html', {'posts': posts})


@login_required
def post_create(request):
    task = request.GET.get('task', '')
    task_time = request.GET.get('task_time', '')
    if request.method == 'POST':
        form = PostForm(request.POST, initial={'task': task, 'task_time': task_time})
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm(initial={'task': task, 'task_time': task_time})
    return render(request, 'community/post_form.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
    return redirect('post_list')