import markdown
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ArticlePostForm
from .models import *


# Views here.

def test_hello_word(request):
    """A simple HelloWorld test,return USER_AGENT for example"""
    return HttpResponse("Your user agent:" + str(request.META['HTTP_USER_AGENT']))


def show_article(request):
    """展示所有发布的文章"""
    article_list = ArticleStorage.objects.filter(if_publish=True)
    # 传递给模板的对象
    # TODO:修复markdown在预览界面的显示问题
    show_article_context = {'articles': article_list}
    return render(request, template_name='article/list.html', context=show_article_context)


def article_detail(request, article_id):
    """获得指定id的文章"""
    selected_article = ArticleStorage.objects.get(id=article_id)
    # 该文章不可见时进行屏蔽处理
    # TODO:创建单独的屏蔽页面
    if selected_article.if_publish:
        selected_article.text = markdown.markdown(selected_article.text,
                                                  extensions=[
                                                      # 缩写,表格等常用扩展
                                                      'markdown.extensions.extra',
                                                      # 语法高亮扩展
                                                      'markdown.extensions.codehilite',
                                                  ])
    else:
        selected_article.text = '该文章不可见！'
    # 传递给模板的对象
    detail_context = {'article': selected_article}
    return render(request, template_name='article/detail.html', context=detail_context)


def article_create(request):
    """处理文章提交和创建"""
    if request.method == 'POST':
        # 存储提交的POST数据
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的POST是否满足要求
        if article_post_form.is_valid():
            # 创建提交到数据库的对象(暂不提交)
            add_new_article = article_post_form.save(commit=False)
            # 指定id = 1的用户为作者
            # TODO:修改判断用户的逻辑
            add_new_article.author = User.objects.get(id=1)
            add_new_article.save()
            return redirect('article:show_article')
        else:
            return HttpResponse("创建表单格式错误！")
    else:
        # 创建空表单实例
        article_post_form = ArticlePostForm()
        create_context = {'article_post_form': article_post_form}
        return render(request, template_name='article/create.html', context=create_context)


def article_delete(request, article_id):
    # TODO:限制用户删除文章
    if request.method == 'POST':
        select_article = ArticleStorage.objects.get(id=article_id)
        select_article.delete()
        return redirect('article:show_article')
    else:
        return HttpResponse("删除请求格式错误！")


def article_update(request, article_id):
    select_article = ArticleStorage.objects.get(id=article_id)
    if request.method == 'POST':
        # 存储提交的POST数据
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            select_article.title = request.POST['title']
            select_article.text = request.POST['text']
            select_article.if_publish = article_post_form.cleaned_data['if_publish']
            select_article.save()
            return redirect("article:article_detail", article_id=article_id)
        else:
            return HttpResponse("修改表单格式错误！")
    else:
        article_post_form = ArticlePostForm()
        update_context = {'article': select_article, 'article_post_form': article_post_form}
        # 将响应返回到模板中
        return render(request, 'article/update.html', update_context)
