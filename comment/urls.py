from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('post-comment/<int:article_id>/', views.post_comment, name='post-comment')
]
