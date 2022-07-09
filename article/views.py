from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import markdown


# Views here.

def test_hello_word(request):
    """A simple HelloWorld test,return USER_AGENT for example"""
    return HttpResponse("Your user agent:"+str(request.META['HTTP_USER_AGENT']))


def show_article(request):
    """展示所有发布的文章"""
    article_list = ArticleStorage.objects.filter(if_publish=True)
    # 传递给模板的对象
    show_article_context = {'articles': article_list}
    return render(request, template_name='article/list.html', context=show_article_context)


def article_detail(request, article_id):
    """获得指定id的文章"""
    selected_article = ArticleStorage.objects.get(id=article_id)
    # 该文章不可见时进行屏蔽处理
    if selected_article.if_publish is False:
        response = HttpResponse("404 Not Found.Your user agent:"+str(request.META['HTTP_USER_AGENT']))
        response.status_code = 404
        return response
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
