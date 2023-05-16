from django import forms
from .models import Post, Comment
from django.core.exceptions import ValidationError


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


class KellyForm(forms.Form):
    probability = forms.FloatField(required=True)
    win = forms.FloatField(required=True)
    loss = forms.FloatField(required=True)

    def clean_probability(self):
        data = self.cleaned_data['probability']

        if not isinstance(data, float):
            raise ValidationError('소수점 형태로 입력해주십시오')

        if data > 1.0:
            raise ValidationError('최대값을 1.0 입니다')
        return abs(data)

    def clean_win(self):
        data = self.cleaned_data['win']
        if not isinstance(data, float):
            raise ValidationError('소수점 형태로 입력해주십시오')
        return abs(data)

    def clean_loss(self):
        data = self.cleaned_data['loss']
        if not isinstance(data, float):
            raise ValidationError('소수점 형태로 입력해주십시오')
        return abs(data)
