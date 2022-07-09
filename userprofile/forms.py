from django import forms
from .models import *


# 登录表单
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
