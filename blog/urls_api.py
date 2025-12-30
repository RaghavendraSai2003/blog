from django.urls import path
from .api_views import get_posts, get_single_post, create_post , delete_post, protected_view

urlpatterns = [
    path('posts/', get_posts),
    path('posts/create/', create_post),
    path('posts/<slug:slug>/', get_single_post),
    path('posts/<slug:slug>/delete/', delete_post),
    path('protected/', protected_view),
]
