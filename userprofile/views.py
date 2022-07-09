from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm


# Create your views here.


def user_login(request):
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
                return HttpResponse("账号或密码输入有误。请重新输入~")
        else:
            return HttpResponse("登录表单提交错误！")
    else:
        user_login_form = UserLoginForm()
        login_context = {'login_form': user_login_form}
        return render(request, template_name='userprofile/login.html', context=login_context)


def user_logout(request):
    logout(request)
    return redirect("article:show_article")
