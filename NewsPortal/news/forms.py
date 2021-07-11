from django.forms import ModelForm
from .models import Post, Category
from django import forms


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'author', 'category_type', 'text']


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = []