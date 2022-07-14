from django.contrib import admin
from .models import ArticleStorage, ArticleColumn

# Register your models here.

admin.site.register(ArticleStorage)
admin.site.register(ArticleColumn)