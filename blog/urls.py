from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .auth_views import custom_login
from .auth_views import register_user
from .views import protected_view, writer_dashboard, reader_dashboard, create_post

urlpatterns = [
    path("",views.StartingPageView.as_view(),name='starting-page'),
    path("posts",views.AllPostView.as_view(),name='posts-page'),
    path('posts/<slug:slug>',views.SinglePostView.as_view(),name="post-detail-page"),
    path("read-later", views.ReadLaterView.as_view(), name="read-later"),
     path("register/", register_user, name="register"),
     path("dashboard/writer/", writer_dashboard, name="writer-dashboard"),
path("dashboard/reader/", reader_dashboard, name="reader-dashboard"),
    path("create-post/", create_post, name="create-post"),
    path("myposts/", views.manage_posts, name="manage-posts"),
    path("post/<slug:slug>/delete", views.delete_post, name="delete-post"),
    path('protected/', protected_view, name='protected'),
    path("posts/", views.AllPostView.as_view(), name="posts-page"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
