import markdown
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ArticlePostForm
from .models import *
from userprofile.models import Profile


def test_hello_word(request):
    """A simple HelloWorld test,return USER_AGENT for example"""
    return HttpResponse("Your user agent:" + str(request.META['HTTP_USER_AGENT']))


def show_article(request):
    """展示所有发布的文章"""
    article_list = ArticleStorage.objects.filter(if_publish=True)
    paginator = Paginator(article_list, 6)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    # 传递给模板的对象
    # TODO:修复markdown在预览界面的显示问题
    show_article_context = {'articles': articles}
    return render(request, template_name='article/list.html', context=show_article_context)


def article_detail(request, article_id):
    """获得指定id的文章"""
    selected_article = ArticleStorage.objects.get(id=article_id)
    profile = Profile.objects.get(user_id=request.user.id)
    # 该文章不可见时进行屏蔽处理
    # TODO:创建单独的屏蔽页面
    if selected_article.if_publish:
        selected_article.text = markdown.markdown(selected_article.text,
                                                  extensions=[
                                                      # 缩写,表格等常用扩展
                                                      'markdown.extensions.extra',
                                                      # 语法高亮扩展
                                                      'markdown.extensions.codehilite',
                                                      # 标题扩展
                                                      'markdown.extensions.toc',
                                                  ])
    else:
        selected_article.text = '该文章不可见！'
    if request.user.is_superuser and profile.author_permission:
        permission_grade = 4
    elif selected_article.author == request.user and profile.author_permission:
        permission_grade = 1
    else:
        permission_grade = 0
    # 传递给模板的对象
    detail_context = {'article': selected_article, 'permission_grade': permission_grade}
    return render(request, template_name='article/detail.html', context=detail_context)


@login_required
def article_create(request):
    """处理文章创建"""
    error_msg = ""
    create_user = request.user
    profile = Profile.objects.get(user_id=create_user.id)
    if not profile.author_permission:
        return redirect('article:show_article')
    if request.method == 'POST':
        # 存储提交的POST数据
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的POST是否满足要求
        if article_post_form.is_valid():
            # 创建提交到数据库的对象(暂不提交)
            add_new_article = article_post_form.save(commit=False)
            # 指定提交的用户为作者
            add_new_article.author = create_user
            add_new_article.save()
            return redirect('article:show_article')
        else:
            error_msg = "创建表单格式错误！"
    article_post_form = ArticlePostForm()
    create_context = {'article_post_form': article_post_form, 'error_msg': error_msg}
    return render(request, template_name='article/create.html', context=create_context)


@login_required
def article_delete(request, article_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if request.method == 'POST' and profile.author_permission:
        select_article = ArticleStorage.objects.get(id=article_id)
        if select_article.author == request.user or request.user.is_superuser:
            select_article.delete()
            return redirect('article:show_article')
    return redirect("article:article_detail", article_id=article_id)


@login_required
def article_update(request, article_id):
    error_msg = ""
    select_article = ArticleStorage.objects.get(id=article_id)
    profile = Profile.objects.get(user_id=request.user.id)
    if not (profile.author_permission and (select_article.author == request.user or request.user.is_superuser)):
        return redirect("article:article_detail", article_id=article_id)
    if request.method == 'POST':
        # 存储提交的POST数据
        article_post_form = ArticlePostForm(data=request.POST, instance=select_article)
        if article_post_form.is_valid():
            article_post_form.save()
            return redirect("article:article_detail", article_id=article_id)
        else:
            error_msg = "文章格式错误，请重新编辑！"
    article_post_form = ArticlePostForm()
    update_context = {'article': select_article, 'article_post_form': article_post_form, 'error_msg': error_msg}
    # 将响应返回到模板中
    return render(request, 'article/update.html', update_context)
