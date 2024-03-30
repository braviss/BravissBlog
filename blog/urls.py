from django.urls import path
from blog import views
from blog.views import update_publish_date

urlpatterns = [
    path('articles',
         views.ArticleListView.as_view(),
         name='article_list'),
    path('users/<str:username>/articles/',
         views.UserArticleListView.as_view(),
         name='user_articles'),
    path('articles/<slug:slug>',
         views.ArticleDetailView.as_view(),
         name='article_detail'),
    path('article/create',
         views.ArticleCreateView.as_view(),
         name='article_create'),
    path('article/update/<slug:slug>/',
         views.ArticleUpdateView.as_view(),
         name='article_update'),
    path('article/delete/<slug:slug>',
         views.ArticleDeleteView.as_view(),
         name='article_delete'),

    path('article/raise/<slug:slug>',
         views.ArticleRaiseView.as_view(),
         name='article_raise'),

    path('update_publish_date/<slug:slug>/',
         update_publish_date,
         name='update_publish_date'),
]
