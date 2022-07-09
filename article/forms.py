from django import forms
from .models import ArticleStorage


class ArticlePostForm(forms.ModelForm):
    """写文章的表单类"""

    class Meta:
        # 表明数据模型的来源
        model = ArticleStorage
        # 定义提交表单中的字段
        fields = ('title', 'text', 'if_publish')
