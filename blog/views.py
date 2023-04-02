import os
from uuid import uuid4
from django.http import JsonResponse, Http404
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Post, Category, Comment, Tag, Series
from .forms import PostForm, CommentForm


def post_list(request):
    posts = Post.objects.filter(
        category__is_publish=True, # 공개 카테고리
        published_date__lte=timezone.now() # 발행된 글
    ).order_by('-published_date') # 최근 발행글이 가장 앞에 오도록 정렬

    page = request.GET.get('page')
    posts_per_page = settings.POSTS_PER_PAGE # 페이지당 포스트 개수
    paginator = Paginator(posts, posts_per_page)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)

    left_index = (int(page) - 2)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 2)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages

    page_range = range(left_index, right_index + 1)
    return render(request, 'blog/post_list.html', {'posts': page_obj, 'page_range': page_range, 'paginator': paginator})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if not request.user.is_authenticated:
        if not post.published_date:
            raise Http404('존재하지 않는 포스트입니다.')

    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            cleaned_tags = form.cleaned_data['tags']
            cleaned_series = form.cleaned_data['series']

            post = form.save(commit=False)
            post.author = request.user
            post.save()

            if cleaned_tags:
                tags = cleaned_tags.split(',')
                for tag in tags:
                    strip_tag = tag.strip()
                    if not strip_tag:
                        continue

                    _tag, _ = Tag.objects.get_or_create(name=strip_tag)
                    post.tags.add(_tag)

            if cleaned_series:
                strip_series = cleaned_series.strip()
                if strip_series:
                    _series, _ = Series.objects.get_or_create(name=strip_series)
                    post.series.add(_series)

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    tags = post.tags.all()
    series = post.series.all()

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            cleaned_tags = form.cleaned_data['tags']
            cleaned_series = form.cleaned_data['series']

            post = form.save(commit=False)
            post.author = request.user
            post.save()

            post.tags.clear()
            if cleaned_tags:
                tags = cleaned_tags.split(',')
                for tag in tags:
                    strip_tag = tag.strip()
                    if not strip_tag:
                        continue

                    _tag, _ = Tag.objects.get_or_create(name=strip_tag)
                    post.tags.add(_tag)

            post.series.clear()
            if cleaned_series:
                series_list = cleaned_series.split(',')
                for serie in series_list:
                    strip_serie = serie.strip()
                    if not strip_serie:
                        continue

                    _serie, _ = Series.objects.get_or_create(name=strip_serie)
                    post.series.add(_serie)

            return redirect('post_detail', pk=post.pk)
    else:
        tag_list = list()
        for tag in tags:
            tag_list.append(tag.name)
        tag_str = ', '.join(tag_list)

        series_list = list()
        for serie in series:
            series_list.append(serie.name)
        series_str = ', '.join(series_list)

        form = PostForm(instance=post, initial={'tags':tag_str, 'series': series_str})
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')

    page = request.GET.get('page')
    posts_per_page = settings.POSTS_PER_PAGE # 페이지당 포스트 개수
    paginator = Paginator(posts, posts_per_page)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)

    left_index = (int(page) - 2)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 2)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages

    page_range = range(left_index, right_index + 1)
    return render(request, 'blog/post_draft_list.html', {'posts': page_obj, 'page_range': page_range, 'paginator': paginator})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=post.pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

@csrf_exempt
def upload_image(request):
    if request.method != "POST":
        return JsonResponse({'Error Message': "Wrong request"})

    # If it's not series and not article, handle it differently
  

    file_obj = request.FILES['file']
    file_name_suffix = file_obj.name.split(".")[-1]
    if file_name_suffix not in ["jpg", "png", "gif", "jpeg"]:
        return JsonResponse({"Error Message": f"Wrong file suffix ({file_name_suffix}), supported are .jpg, .png, .gif, .jpeg"})

    file_path = os.path.join(settings.MEDIA_ROOT, 'blog', file_obj.name)
    
    if os.path.exists(file_path):
        file_obj.name = str(uuid4()) + '.' + file_name_suffix
        file_path = os.path.join(settings.MEDIA_ROOT, 'blog', file_obj.name)

    with open(file_path, 'wb+') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)

        return JsonResponse({
            'message': 'Image uploaded successfully',
            'location': os.path.join(settings.MEDIA_URL, 'blog',  file_obj.name)
        })   


# category_detail
def category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if not request.user.is_authenticated:
        if not category.is_publish:
            raise Http404('존재하지 않는 카테고리 입니다.')

    posts = category.posts.filter(published_date__isnull=False).order_by('-published_date')

    page = request.GET.get('page')
    posts_per_page = settings.POSTS_PER_PAGE # 페이지당 포스트 개수
    paginator = Paginator(posts, posts_per_page)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)

    left_index = (int(page) - 2)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 2)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages

    page_range = range(left_index, right_index + 1)
    return render(request, 'blog/category.html', {'posts': page_obj, 'page_range': page_range, 'paginator': paginator})

# tag_detail
def tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    posts = tag.post_set.filter(
        category__is_publish=True, # 공개 카테고리
        published_date__lte=timezone.now() # 발행된 글
    ).order_by('-published_date') # 최근 발행글이 가장 앞에 오도록 정렬

    page = request.GET.get('page')
    posts_per_page = settings.POSTS_PER_PAGE # 페이지당 포스트 개수
    paginator = Paginator(posts, posts_per_page)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)

    left_index = (int(page) - 2)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 2)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages

    page_range = range(left_index, right_index + 1)
    return render(request, 'blog/post_list.html', {'posts': page_obj, 'page_range': page_range, 'paginator': paginator})


# series_detail
def series(request, pk):
    series = get_object_or_404(Series, pk=pk)
    posts = series.post_set.filter(
        category__is_publish=True, # 공개 카테고리
        published_date__lte=timezone.now() # 발행된 글
    ).order_by('-published_date') # 최근 발행글이 가장 앞에 오도록 정렬

    page = request.GET.get('page')
    posts_per_page = settings.POSTS_PER_PAGE # 페이지당 포스트 개수
    paginator = Paginator(posts, posts_per_page)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)

    left_index = (int(page) - 2)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 2)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages

    page_range = range(left_index, right_index + 1)
    return render(request, 'blog/post_list.html', {'posts': page_obj, 'page_range': page_range, 'paginator': paginator})

