from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    tags = forms.CharField(label='태그', max_length=200, required=False)
    series = forms.CharField(label='시리즈', max_length=200, required=False)

    class Meta:
        model = Post
        fields = ('category', 'title', 'text', )
        labels = {
            "category": "카테고리",
            "title": "제목",
            "text": "내용",
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
        widgets = {
            'text': forms.TextInput(attrs={'size': '100'})
        }
        labels = {
            "author": "이름",
            "text": "내용",
        }

