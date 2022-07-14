from django.urls import path

from . import views

app_name = 'userprofile'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('delete/', views.user_delete, name='delete'),
    path('edit/', views.profile_edit, name='edit'),
    path('userinfo/<int:show_user_id>', views.profile_show, name='userinfo'),
]
