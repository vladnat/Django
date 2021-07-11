from django.shortcuts import render, reverse, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.core.paginator import Paginator
from .models import Author, Post, User, Category
from datetime import datetime
from .filter import PostFilter
from .forms import PostForm, CategoryForm  # импортируем нашу форму
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives, mail_admins, send_mail


class CategoryAdd(CreateView):
    template_name = 'subscribe.html'
    model = Category
    queryset = Post.objects.all()
    form_class = CategoryForm


    def post(self, request, *args, **kwargs):
        user = self.request.user
        id = self.kwargs.get('pk')
        Category.objects.get(pk=id).subscribers.add(user)
        return redirect('/')


class CategoryRemove(CreateView):
    template_name = 'unsubscribe.html'
    model = Category
    queryset = Category.objects.all()
    form_class = CategoryForm


    def post(self, request, *args, **kwargs):
        user = self.request.user
        id = self.kwargs.get('pk')
        Category.objects.get(pk=id).subscribers.remove(user)
        return redirect('/')


class AuthorsList(ListView):
    model = Author
    template_name = 'authors.html'
    context_object_name = 'authors'
    queryset = Author.objects.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class AuthorDetail(DetailView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'author'
    queryset = Author.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        user = self.request.user
        context['author'] = Author.objects.get(pk=id).author_user.all()
        return context


class Posts(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-date_creation']
    queryset = Post.objects.all()
    paginate_by = 3  # поставим постраничный вывод в один элемент

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()

        return context


# дженерик для получения деталей о товаре
class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        user = self.request.user
        context['post_categories'] = Post.objects.get(pk=id).post_category.all()
        context['user_categories'] = Category.objects.filter(subscribers=User.objects.get(username=str(user)))
        return context


class SearchPost(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = ['-date_creation']
    paginate_by = 10  # поставим постраничный вывод в один элемент

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data
        # у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        return context


# дженерик для создания объекта.
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post')


# дженерик для редактирования объекта
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'news/post_edit.html'
    form_class = PostForm
    permission_required = ('news.change_post')

# метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся
    # редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'