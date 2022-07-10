from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import *


# Create your views here.


def user_login(request):
    error_msg = ""
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # 取出合法数据
            data = user_login_form.cleaned_data
            # 检测是否匹配数据库中的用户
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect("article:show_article")
            else:
                error_msg = "用户名或密码错误，请重新输入！"
        else:
            error_msg = "输入格式错误，请重新输入！"
    user_login_form = UserLoginForm()
    login_context = {'login_form': user_login_form, 'error_msg': error_msg}
    return render(request, template_name='userprofile/login.html', context=login_context)


def user_logout(request):
    logout(request)
    return redirect("article:show_article")


def user_register(request):
    error_msg = ""
    if request.method == 'POST':
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save()
            login(request, new_user)
            return redirect('article:show_article')
        else:
            error_msg = "用户名或密码格式有误，请重新输入！"
    user_register_form = UserRegisterForm()
    register_context = {'register_form': user_register_form, 'error_msg': error_msg}
    return render(request, template_name='userprofile/register.html', context=register_context)
