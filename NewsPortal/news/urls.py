from django.urls import path
from .views import Posts, SearchPost, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView


urlpatterns = [
    path('', Posts.as_view()),
    path('search', SearchPost.as_view()),
    path('<int:pk>/', PostDetailView.as_view(), name='post'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]