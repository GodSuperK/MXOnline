from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib import auth
from django.views import generic
from django.contrib.auth import hashers

from .forms import LoginForm
from .forms import RegisterForm
from .models import UserProfile


# Create your views here.

class CustomBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception:
            return None


def user_login(request):
    if request.method == "GET":
        return render(request, 'login.html', {})
    elif request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(request, "login.html", {"error_msg": '用户名或密码错误'})
    else:
        pass


class LoginView(generic.View):

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        # 如果提交的数据满足django表单预定义，则返回True
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect("/")
            else:
                return render(request, "login.html", {"error_msg": '用户名或密码错误'})
        else:
            # 将表单传回前端，使用模板语言提取错误信息
            return render(request, "login.html", {"login_form": login_form})


class RegisterView(generic.View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        """用户邮箱注册逻辑"""
        # 1. 先使用注册表单验证数据字段是否有效
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get("email", "")
            password = request.POST.get("password", "")
            # TODO 对邮箱进行数据库查询，是否已经注册
            # 实例化一个UserProfile对象，然后保存到数据库
            user = UserProfile()
            user.email = email
            # 将用户名暂时初始化为邮箱
            user.username = email
            # 对密码进行加密，保存密文
            user.password = hashers.make_password(password=password)
            # 为用户注册账户，但并为激活账号
            user.save()
            # TODO 发送邮箱激活链接

        return render(request, "register.html", {'register_form': register_form})
