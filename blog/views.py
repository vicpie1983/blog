from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Category
from .forms import PostForm


def post_list(request):
    posts = Post.objects.filter(
        category__is_publish=True, # 공개 카테고리
        published_date__lte=timezone.now() # 발행된 글
    ).order_by('-published_date') # 최근 발행글이 가장 앞에 오도록 정렬

    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            print('type:',type(post))
            print('post.pk:', post.pk)
            post.save()
            print('post.pk:', post.pk)
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
