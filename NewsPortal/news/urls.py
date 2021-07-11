from django.urls import path
from .views import Posts, SearchPost, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, AuthorsList
from .views import AuthorDetail, CategoryAdd, CategoryRemove


urlpatterns = [
    path('', Posts.as_view()),
    path('search', SearchPost.as_view()),
    path('<int:pk>/', PostDetailView.as_view(), name='post'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('authors', AuthorsList.as_view()),
    path('authors/<int:pk>/', AuthorDetail.as_view()),
    path('subscribe/<int:pk>', CategoryAdd.as_view(), name='subscribe'),
    path('unsubscribe/<int:pk>', CategoryRemove.as_view(), name='unsubscribe'),
]