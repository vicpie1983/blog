from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category


def post_list(request):
    categorys = Category.objects.filter(is_publish=True).order_by('ordering')

    posts = Post.objects.filter(
        category__is_publish=True, # 공개 카테고리
        published_date__lte=timezone.now() # 발행된 글
    ).order_by('-published_date') # 최근 발행글이 가장 앞에 오도록 정렬

    return render(request, 'blog/post_list.html', {'categorys': categorys, 'posts': posts})


def post_detail(request, pk):
    categorys = Category.objects.filter(is_publish=True).order_by('ordering')

    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'categorys': categorys, 'post': post})

