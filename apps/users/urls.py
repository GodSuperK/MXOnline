__author__ = "GodSuperK"
__date__ = "18-10-25 上午8:48"

from django.urls import path, re_path
from . import views

app_name = "user"
urlpatterns = [

    path('login/', views.LoginView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('active/<str:code>/', views.ActiveUserView.as_view(), name="active"),
    path('forgetpwd/', views.ForgetPwdView.as_view(), name="forgetpwd"),
    path('pwd_reset/', views.PasswordResetView.as_view(), name="pwdreset"),

]
