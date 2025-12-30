from django import forms
from .models import Comment
from .models import Post
from blog.models import Tag
from blog.models import Author
class CommentForm(forms.ModelForm):
  class Meta:
   model= Comment
   exclude=["post"]
   labels={
     "user_name":"Your Name",
     "user_email":"Your Email",
     "text":"Your Comment"
   }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['date']   # do NOT include auto_now fields

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "excerpt": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "author": forms.Select(attrs={"class": "form-control"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control", "size": 5}),
        }