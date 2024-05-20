from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_create, name='post_create'),
    path('accounts/signup/', views.signup, name='signup'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
]
