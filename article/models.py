from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from taggit.managers import TaggableManager

# ---tips---
# 修改模型后，需要使用 python manage.py makemigrations 记录修改为一次迁移
# 再使用 python manage.py migrate 将迁移应用到数据库中
class ArticleColumn(models.Model):
    """博客栏目分类"""
    title = models.CharField(max_length=100, blank=True, unique=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        """定义栏目的元数据"""
        verbose_name = '栏目'
        verbose_name_plural = '栏目'
        # 数据排序方式:created_time倒序，再以author正序
        ordering = ['title']

    def __str__(self):
        return self.title


class ArticleStorage(models.Model):
    """博客文章数据模型/库"""

    # 文章作者
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    # 文章标题
    title = models.CharField(max_length=80)
    # 文章概述
    overview = models.CharField(max_length=100, blank=True)
    # 文章正文
    text = models.TextField()
    # 文章创建时间
    created_time = models.DateTimeField(default=timezone.now)
    # 文章更新时间
    updated_time = models.DateTimeField(auto_now=True)
    # 文章是否公开
    if_publish = models.BooleanField(default=True)
    # 文章标签
    # tags = TaggableManager(blank=True)

    # 活动开始时间
    com_start_time = models.DateTimeField(default=timezone.now)
    # 活动结束时间
    com_end_time = models.DateTimeField(default=timezone.now)
    # 活动地点
    com_location = models.CharField(max_length=100, blank=True)
    # 活动限制
    com_limit = models.CharField(max_length=100, blank=True)
    # 活动是否可以组队
    com_if_group = models.BooleanField(default=False)

    # 所属栏目
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    class Meta:
        """定义数据库模型的元数据"""
        verbose_name = '活动'
        verbose_name_plural = '活动'
        # 数据排序方式:created_time倒序，再以author正序
        ordering = ['-created_time', 'author']

    def __str__(self) -> str:
        """调用文章的str()时返回文章标题"""
        # 返回文章标题
        return str(self.title) + '@' + str(self.author)

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])
