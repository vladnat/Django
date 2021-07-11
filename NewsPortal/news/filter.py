from django_filters import FilterSet  # импортируем filterset, чем-то напоминающий знакомые дженерики
from django.forms import DateInput
import django_filters
from .models import Post



class PostFilter(FilterSet):
    date_creation = django_filters.DateFilter(field_name='date_creation', widget=DateInput(attrs={'type': 'date'}), lookup_expr='gt', label='Позже даты')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Заголовок')
    # author_name = django_filters.CharFilter(field_name='author_id__author_user_id__username', lookup_expr='c', label='Автор')
    # post_category = django_filters.CharFilter(field_name='post_category__name', lookup_expr='icontains', label='Категория')

    class Meta:
        model = Post
        fields = {
                    'author': ['exact'],
                    'post_category': ['exact'],
                    }