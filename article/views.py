from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import markdown


# Views here.

def test_hello_word(request):
    """A simple HelloWorld test,return USER_AGENT for example"""
    return HttpResponse(str(request.META['HTTP_USER_AGENT']))


def show_article(request):
    """展示所有文章"""
    article_list = ArticleStorage.objects.all()
    # 传递给模板的对象
    show_article_context = {'articles': article_list}
    return render(request, template_name='article/list.html', context=show_article_context)


def article_detail(request, article_id):
    """获得指定id的文章"""
    selected_article = ArticleStorage.objects.get(id=article_id)
    selected_article.text = markdown.markdown(selected_article.text,
                                              extensions=[
                                                  # 缩写,表格等常用扩展
                                                  'markdown.extensions.extra',
                                                  # 语法高亮扩展
                                                  'markdown.extensions.codehilite',
                                              ])
    # 传递给模板的对象
    detail_context = {'article': selected_article}
    return render(request, template_name='article/detail.html', context=detail_context)
