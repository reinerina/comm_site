from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.CharField(max_length=200, default='')
    task_time = models.CharField(max_length=200, default='')

    class Meta:
        db_table = 'article_tb'  #定义表名
        verbose_name = '文章'  #后台显示
        verbose_name_plural = verbose_name  #后台显示的复数

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment_tb'
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
