from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import PostForm, CommentForm
from .models import Post, Comment


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
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'community/post_detail.html', {'post': post, 'comments': comments, 'form': form})


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
        post.comments.all().delete()
        post.delete()
    return redirect('post_list')

@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('post_detail', post_id=post_id)


@login_required
def like_item(request, item_type, item_id):
    if item_type == 'post':
        item = get_object_or_404(Post, id=item_id)
    elif item_type == 'comment':
        item = get_object_or_404(Comment, id=item_id)
    else:
        return JsonResponse({'error': 'Invalid item type'}, status=400)

    if item.likes.filter(id=request.user.id).exists():
        item.likes.remove(request.user)
        liked = False
    else:
        item.likes.add(request.user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'total_likes': item.total_likes(),
        'item_id': item_id,
        'item_type': item_type
    })


def logout_user(request):
    logout(request)
    return redirect('post_list')
