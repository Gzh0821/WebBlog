import markdown
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ArticlePostForm
from .models import *
from userprofile.models import Profile
from comment.models import Comment


# 主页
def home_page(request):
    return redirect("article:show_article")


def test_hello_word(request):
    """A simple HelloWorld test,return USER_AGENT for example"""
    return HttpResponse("Your user agent:" + str(request.META['HTTP_USER_AGENT']))


def show_article(request, selected_column=None):
    """展示所有发布的文章"""
    search = request.GET.get('search')
    show_collect = request.GET.get('collect')
    if request.user.is_authenticated and show_collect:
        profile = Profile.objects.get(user_id=request.user.id)
        article_list = profile.collected_com.all()
    else:
        article_list = ArticleStorage.objects.all()
    if search:
        # 进行搜索
        # article_list = ArticleStorage.objects.filter(Q(title__icontains=search) |
        #                                              Q(text__icontains=search) |
        #                                              Q(overview__icontains=search))
        article_list = article_list.filter(Q(title__icontains=search) |
                                           Q(text__icontains=search) |
                                           Q(overview__icontains=search))
    else:
        search = ''
        # article_list = ArticleStorage.objects.all()

    if selected_column:
        column = get_object_or_404(ArticleColumn, id=selected_column)
        article_list = article_list.filter(column_id=column)
    else:
        column = ArticleColumn.objects.none()

    paginator = Paginator(article_list, 6)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    all_column = ArticleColumn.objects.all()
    # 传递给模板的对象
    show_article_context = {'articles': articles, 'search': search, 'show_collect': show_collect,
                            'all_column': all_column, 'now_column': column}
    return render(request, template_name='article/list.html', context=show_article_context)


def article_detail(request, article_id):
    """获得指定id的文章"""
    error_msg = ""
    if_collected = False
    selected_article = get_object_or_404(ArticleStorage, id=article_id)
    # 该文章不可见时进行屏蔽处理
    # TODO:创建单独的屏蔽页面
    article_markdown = markdown.Markdown(
        extensions=[
            # 缩写,表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 标题扩展
            'markdown.extensions.toc',
            'markdown.extensions.nl2br'
        ])
    # 若文章未公开，显示未公开信息
    if not selected_article.if_publish:
        error_msg = '该活动未被公开'

    # 若文章已公开，显示未公开信息
    if not request.user.is_authenticated:
        permission_grade = -1
        comment_permission = False
    else:
        profile = Profile.objects.get(user_id=request.user.id)
        if_collected = profile.collected_com.filter(id=article_id).exists()
        comment_permission = profile.comment_permission
        if not profile.author_permission:
            permission_grade = 0
        else:
            permission_grade = 4 if request.user.is_superuser else (1 if selected_article.author == request.user else 0)
    # 传递给模板的对象
    if selected_article.if_publish or request.user.is_superuser or selected_article.author == request.user:
        selected_article.text = article_markdown.convert(selected_article.text)
        comments = Comment.objects.filter(article=article_id)
    else:
        selected_article.text = '该文章未被公开！'
        comments = Comment.objects.none()
    # 是否已收藏

    detail_context = {'article': selected_article,
                      'user': request.user,
                      'if_collected': if_collected,
                      'permission_grade': permission_grade,
                      'comment_permission': comment_permission,
                      'toc': article_markdown.toc,
                      'comments': comments,
                      'error_msg': error_msg}
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
            # article_post_form.save_m2m()
            return redirect(add_new_article)
        else:
            error_msg = "创建表单格式错误！"
    article_post_form = ArticlePostForm()
    columns = ArticleColumn.objects.all()
    create_context = {'article_post_form': article_post_form,
                      'error_msg': error_msg,
                      'columns': columns}
    return render(request, template_name='article/create.html', context=create_context)


@login_required
def article_delete(request, article_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if request.method == 'POST' and profile.author_permission:
        select_article = get_object_or_404(ArticleStorage, id=article_id)
        if select_article.author == request.user or request.user.is_superuser:
            select_article.delete()
            return redirect('article:show_article')
    return redirect("article:article_detail", article_id=article_id)


@login_required
def article_update(request, article_id):
    error_msg = ""
    select_article = get_object_or_404(ArticleStorage, id=article_id)
    profile = Profile.objects.get(user_id=request.user.id)
    if not (profile.author_permission and (select_article.author == request.user or request.user.is_superuser)):
        return redirect("article:article_detail", article_id=article_id)
    if request.method == 'POST':
        # 存储提交的POST数据
        article_post_form = ArticlePostForm(data=request.POST, instance=select_article)
        if article_post_form.is_valid():
            article_post_form.save()
            # article_post_form.save_m2m()
            return redirect("article:article_detail", article_id=article_id)
        else:
            error_msg = "文章格式错误，请重新编辑！"
    article_post_form = ArticlePostForm()
    columns = ArticleColumn.objects.all()
    update_context = {'article': select_article,
                      'article_post_form': article_post_form,
                      'error_msg': error_msg,
                      'columns': columns}
    # 将响应返回到模板中
    return render(request, 'article/update.html', update_context)


@login_required
def article_collect(request, article_id):
    profile = Profile.objects.get(user_id=request.user.id)
    select_article = get_object_or_404(ArticleStorage, id=article_id)
    profile.collected_com.add(select_article)
    return redirect("article:article_detail", article_id=article_id)


@login_required
def article_cancel_collect(request, article_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        select_article = get_object_or_404(ArticleStorage, id=article_id)
        profile.collected_com.remove(select_article)
    return redirect("article:article_detail", article_id=article_id)
