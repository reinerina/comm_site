from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_create, name='post_create'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/logout/', views.logout_user, name='logout'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),  # 添加帖子详细页面的URL模式
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
]
