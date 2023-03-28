from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('category', 'title', 'text',)
        labels = {
            "category": "카테고리",
            "title": "제목",
            "text": "내용",
        }
