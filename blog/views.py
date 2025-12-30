from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic import DetailView
from datetime import date
from django.contrib.auth import login
from.models import Post
from.forms import CommentForm,PostForm
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from .models import Profile, Author
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
# Create your views here.



def get_date(post):
    return post['date']


class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name="posts"

    def get_queryset(self):
        queryset= super().get_queryset()
        data=queryset[:3]
        return data
    
class AllPostView(ListView):
    template_name="blog/all-posts.html"
    model=Post
    ordering=["-date"]
    context_object_name="all_posts"

class SinglePostView(DetailView):
    template_name = "blog/post-detail-page.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        context["post_tags"] = post.tags.all()
        context["comment_form"] = CommentForm()
        context["comments"] = post.comments.all().order_by("-id")
        return context

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            # ✅ AJAX response
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "user": comment.user_name,
                    "text": comment.text
                })

            # ✅ Normal form submit
            return redirect("post-detail-page", slug=slug)

        # ❌ Form invalid
        context = self.get_context_data()
        context["comment_form"] = form
        return render(request, self.template_name, context)

   

class ReadLaterView(View):

    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}

        if not stored_posts:      # If None or empty list
            context["posts"] = []
            context["has_posts"] = False

        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-post.html", context)

    def post(self, request):
        stored_posts = request.session.get('stored_posts')

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session['stored_posts'] = stored_posts

        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

@login_required
def create_post(request):
    try:
        author_obj = Author.objects.get(user=request.user)
    except Author.DoesNotExist:
        return HttpResponse("Author profile not created for this user", status=400)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = author_obj
            post.save()
            form.save_m2m()
            return redirect("posts-page")

    else:
        form = PostForm()

    return render(request, "blog/create_post.html", {"form": form})


@login_required
def writer_dashboard(request):
    if request.user.profile.role != "writer":
        return HttpResponse("Access Denied", status=403)

    author = Author.objects.filter(user=request.user).first()

    if not author:
        # Self-healing: Create Author profile if missing
        author = Author.objects.create(
            user=request.user,
            first_name=request.user.username,
            email_address=request.user.email
        )

    posts = Post.objects.filter(author=author)

    return render(request, "blog/writer_dashboard.html", {"posts": posts})




@login_required
def reader_dashboard(request):
    if request.user.profile.role != "reader":
        return HttpResponse("Access Denied", status=403)

    stored_posts = request.session.get("stored_posts", [])
    posts = Post.objects.filter(id__in=stored_posts)

    return render(request, "blog/reader_dashboard.html", {"posts": posts})


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')  # or render the template again

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('login')  # redirect to your login page

    return render(request, 'blog/register.html')


@login_required
def manage_posts(request):
    if request.user.profile.role != "writer":
        return HttpResponse("Access Denied", status=403)
    
    author = Author.objects.filter(user=request.user).first()
    if not author:
        return redirect("writer-dashboard")

    posts = Post.objects.filter(author=author).order_by('-date')
    return render(request, "blog/manage_posts.html", {"posts": posts})


@login_required
def delete_post(request, slug):
    if request.user.profile.role != "writer":
        return HttpResponse("Access Denied", status=403)
        
    author = Author.objects.get(user=request.user)
    post = get_object_or_404(Post, slug=slug, author=author)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect("manage-posts")
    
    return redirect("manage-posts")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"user": request.user.username})
 