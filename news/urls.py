from django.urls import path, include
from .views import (
    NewsListView, ArticlesListView, PostSearchView, PostDetail,
    NewsCreate, ArticleCreate, NewsUpdate, ArticleUpdate,
    NewsDelete, ArticleDelete, upgrade, IndexView, subscribe_to_category,
    unsubscribe_from_category
)
from django.views.decorators.cache import cache_page


urlpatterns = [
    # Новости
    path('', cache_page(60)(NewsListView.as_view()), name='news_list'),
    path('search/', PostSearchView.as_view(), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/', cache_page(300)(PostDetail.as_view()), name='post_detail'),
    path('<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

    # Статьи
    path('articles/', cache_page(300)(ArticlesListView.as_view()), name='articles_list'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),

    # Аутентификация и профиль
    path('upgrade/', upgrade, name='upgrade'),
    path('profile/', IndexView.as_view(), name='protect_index'),
    path('category/<int:category_id>/subscribe/', subscribe_to_category, name='subscribe_category'),
    path('category/<int:category_id>/unsubscribe/', unsubscribe_from_category, name='unsubscribe_category'),



]