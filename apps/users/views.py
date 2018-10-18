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
from .forms import ForgetPwdForm
from .forms import PwdResetForm
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
                return render(request, "login.html", {"login_form": login_form, "error_msg": '用户名或密码错误'})
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

            # 对邮箱进行数据库查询，查询是否已经注册
            u = UserProfile.objects.filter(email=email).first()
            if u:
                return render(request, 'register.html', {"register_form": register_form, "error_msg": '该邮箱已经注册'})

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
        # 1. 数据库查询, 使用get查询，如果结果为空会报错
        email_is_exist = EmailVerifyCode.objects.filter(code=code).first()
        if email_is_exist:
            if email_is_exist.send_type == "register":
                # 2. 将该邮箱所属的账户激活
                user = UserProfile.objects.get(email=email_is_exist.email)
                user.is_active = True
                user.save()
                # 3. 删除该记录，以防止用户重复激活
                email_is_exist.delete()
                # 4. 跳转到用户个人中心或者首页,登陆页面
                return HttpResponse("您的账户已经成功激活")
            elif email_is_exist.send_type == "forget":
                # 查询用户的email
                user = UserProfile.objects.get(email=email_is_exist.email)
                # 跳转到修改密码页面
                return render(request, "password_reset.html", {'email': user.email})
        else:
            return HttpResponse("链接失效")


class ForgetPwdView(generic.View):

    def get(self, request):
        """请求忘记密码表单"""
        forgetpwd_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get("email", '')
            # 1. 数据库查询该邮箱是否存在
            user = UserProfile.objects.filter(email=email).first()
            if user:
                # 2. 如果存在，向该邮箱发送找回密码链接
                status_code = email_send.send_email(email, "forget")
                if status_code:
                    return HttpResponse("链接已经发送到您的邮箱，请检查您的收件箱还有垃圾邮件哦")
                else:
                    return HttpResponse("邮件发送失败")
            else:
                # 3. 如果不存在，跳转为忘记密码页面，同时显示错误
                return render(request, 'forgetpwd.html', {"forgetpwd_form": forgetpwd_form, "error_msg": "该邮箱并未注册账户"})
        else:
            return render(request, 'forgetpwd.html', {"forgetpwd_form": forgetpwd_form})


class PasswordResetView(generic.View):

    def get(self, request):
        pwdreset_form = PwdResetForm()
        return render(request, 'password_reset.html', {'pwdreset_form': pwdreset_form})

    def post(self, request):
        pwdreset_form = PwdResetForm(request.POST)
        email = request.POST.get("email")
        if pwdreset_form.is_valid():
            # 1. 提取数据字段密码以及 邮箱（作为数据库查询依据）
            password = request.POST.get("password", "1")
            password2 = request.POST.get("password2", "2")
            # 2. 比较密码，如果密码相等，保存密文到数据库
            if password == password2:
                user = UserProfile.objects.filter(email=email).first()
                if user:
                    user.password = hashers.make_password(password=password)
                    user.save()
                    return HttpResponse("您的密码已经修改成功，请重新登陆")
            else:
                return render(request, 'password_reset.html', {'email': email, 'error_msg': "两次密码不匹配"})
        else:
            return render(request, 'password_reset.html', {'email': email, 'pwdreset_form': pwdreset_form})
