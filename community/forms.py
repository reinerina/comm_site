from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'task', 'task_time']
        labels = {
            'title': '标题',
            'content': '内容',
            'task': '任务',
            'task_time': '任务时间'
        }
