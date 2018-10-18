from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib import auth
from django.views import generic
from django.contrib.auth import hashers

from .forms import LoginForm
from .forms import RegisterForm
from .models import UserProfile
from .models import EmailVerifyCode
from utils import email_send


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
                # 只有账户已激活的情况下，才能登陆
                if user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    return render(request, "login.html", {"error_msg": '账户未激活'})
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
            # 2. 提取注册字段
            email = request.POST.get("email", "")
            password = request.POST.get("password", "")
            # TODO 对邮箱进行数据库查询，是否已经注册
            # 3. 实例化一个UserProfile对象，然后保存到数据库
            user = UserProfile()
            user.email = email
            # 将用户名暂时初始化为邮箱
            user.username = email
            # 对密码进行加密，保存密文
            user.password = hashers.make_password(password=password)
            # 不激活账户
            user.is_active = False
            user.save()
            # 4. 发送邮箱激活链接
            status_code = email_send.send_email(email, "register")
            if status_code:
                return HttpResponse("激活链接已发送到您的邮箱")
            else:
                return HttpResponse("无效邮箱，发送激活链接失败")
            # 最后，跳转到登陆页面
            # return HttpResponseRedirect('/login/')
        return render(request, "register.html", {'register_form': register_form})


class ActiveUserView(generic.View):
    """
    激活链接验证 View
    """

    def get(self, request, code):
        # 数据库查询
        email_is_exist = EmailVerifyCode.objects.get(code=code)
        if email_is_exist:
            # 将该邮箱所属的账户激活
            user = UserProfile.objects.get(email=email_is_exist.email)
            user.is_active = True
            user.save()
            # 跳转到用户个人中心或者首页,登陆页面
            return HttpResponseRedirect('/')
        else:
            return HttpResponse("验证失败")
