from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import date, timedelta
# Create your models here.

class Tag(models.Model):
    caption=models.CharField(max_length=10)
    def __str__(self):
        return self.caption

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="author_profile")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    email_address = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()



class Post(models.Model):
    title=models.CharField(max_length=150)
    excerpt=models.CharField(max_length=200)
    image=models.ImageField(upload_to="posts",null=True)
    date=models.DateField(auto_now=True)
    slug= models.SlugField(unique=True,db_index=True)
    content=models.TextField(MinLengthValidator(10))
    author=models.ForeignKey(Author,on_delete=models.SET_NULL,related_name="posts",null=True)
    tags=models.ManyToManyField(Tag)

    def __str__(self):
        return self.title 
    
    def is_recent(self):
        return self.date >= date.today() - timedelta(days=1)


class Comment(models.Model):
    user_name= models.CharField(max_length=200)
    user_email=models.EmailField()
    text= models.TextField(max_length=400)
    post= models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('reader', 'Reader'),
        ('writer', 'Writer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='reader')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


