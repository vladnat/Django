from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.core.paginator import Paginator
from .models import Post, Category
from .filter import PostFilter
from .forms import PostForm  # импортируем нашу форму

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class Posts(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-date_creation']
    paginate_by = 3  # поставим постраничный вывод в один элемент

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# дженерик для получения деталей о товаре
class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post.html'
    queryset = Post.objects.all()


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
