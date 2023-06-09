from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('post/new/upload_image', views.upload_image, name="upload_image"),
    path('post/<int:pk>/edit/upload_image', views.upload_image, name="upload_image"),
    path('category/<int:pk>/', views.category, name='category'),
    path('tag/<int:pk>/', views.tag, name='tag'),
    path('series/', views.series_list, name='series_list'),
    path('series/<int:pk>/', views.series, name='series'),
    path('search/', views.search, name='search'),
    path('kelly/', views.kelly_detail, name='kelly'),
]

