from django.shortcuts import render
from django.utils import timezone
from .models import Post


def post_list(request):
    posts = Post.objects.filter(
        category__is_publish=True, # 공개 카테고리
        published_date__lte=timezone.now() # 발행된 글
    ).order_by('-published_date') # 최근 발행글이 가장 앞에 오도록 정렬
    return render(request, 'blog/post_list.html', {'posts': posts})

