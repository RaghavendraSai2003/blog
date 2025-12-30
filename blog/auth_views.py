from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User   # ✅ IMPORTANT
from .models import Profile, Author


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            try:
                if user.profile.role == "writer":
                    return redirect("writer-dashboard")
                else:
                    return redirect("reader-dashboard")
            except:
                # Fallback if profile doesn't exist or is improperly configured
                return redirect("/blog/") 
    else:
        form = AuthenticationForm()

    return render(request, "blog/login.html", {"form": form})


def custom_logout(request):
    logout(request)
    return redirect("login")


def register_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        role = request.POST["role"]   # reader / writer

        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Update Profile (created by signal)
        user.profile.role = role
        user.profile.save()

        # Create Author profile if Writer
        if role == "writer":
            Author.objects.create(
                user=user,
                first_name=username,
                email_address=email
            )

        return redirect("login")

    return render(request, "blog/register.html")

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
