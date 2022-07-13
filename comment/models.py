from django.db import models
from django.contrib.auth.models import User
from article.models import ArticleStorage


# ---tips---
# 修改模型后，需要使用 python manage.py makemigrations 记录修改为一次迁移
# 再使用 python manage.py migrate 将迁移应用到数据库中
class Comment(models.Model):
    article = models.ForeignKey(
        ArticleStorage,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body[:20]
