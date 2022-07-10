from django.urls import path

from . import views

app_name = 'userprofile'

urlpatterns = [
    # 用户登录
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # 注册功能，默认关闭
    path('register/', views.user_register, name='register'),
    path('delete/', views.user_delete, name='delete')
]
