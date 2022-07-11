from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    """用户扩展模型"""
    # 与User模型的数据一一对应
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 电话号码
    phone = models.CharField(max_length=20, blank=True)
    # 头像
    avatar = models.ImageField(upload_to='avatar/%Y%m%d', blank=True)
    # 简介
    bio = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'user:{self.user.username}'