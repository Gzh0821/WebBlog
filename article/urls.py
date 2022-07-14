from django.urls import path
from . import views

app_name = 'article'
urlpatterns = [
    # A simple HelloWorld test
    path('test/hello/', views.test_hello_word, name='test_hello_world'),
    path('', views.home_page, name='home'),
    path('show-article/', views.show_article, name='show_article'),
    path('show-article/<int:selected_column>', views.show_article, name='show_article_with_column'),
    path('article-detail/<int:article_id>/', views.article_detail, name='article_detail'),
    path('article-create/', views.article_create, name='article_create'),
    path('article-delete/<int:article_id>/', views.article_delete, name='article_delete'),
    path('article-update/<int:article_id>/', views.article_update, name='article_update'),
]
