from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('category', 'title', 'text',)
        labels = {
            "category": "카테고리",
            "title": "제목",
            "text": "내용",
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
        labels = {
            "author": "이름",
            "text": "내용",
        }

