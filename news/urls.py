from django.urls import path
from.views import NewsList, PostDetail

urlpatterns = [
    path('', NewsList.as_view(), name = 'news_list'),
    path('<int:pk>', PostDetail.as_view(),name = 'post_detail'),
]