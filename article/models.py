from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ---tips---
# 修改模型后，需要使用 python manage.py makemigrations article 记录修改为一次迁移
# 再使用 python manage.py migrate 将迁移应用到数据库中
class ArticleStorage(models.Model):
    """博客文章数据模型/库"""

    # 文章作者
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    # 文章标题
    title = models.CharField(max_length=100)
    # 文章正文
    text = models.TextField()
    # 文章创建时间
    created_time = models.DateTimeField(default=timezone.now)
    # 文章更新时间
    updated_time = models.DateTimeField(auto_now=True)
    # 文章是否公开
    if_publish = models.BooleanField(default=True)

    class Meta:
        """定义数据库模型的元数据"""
        verbose_name = '文章'
        verbose_name_plural = '文章'
        # 数据排序方式:created_time倒序，再以author正序
        ordering = ['-created_time', 'author']

    def __str__(self) -> str:
        """调用文章的str()时返回文章标题"""
        # 返回文章标题
        return str(self.title) + '@' + str(self.author)
