from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib import auth

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


def get_index(request):
    if request.method == "GET":
        return render(request, "index.html")


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
