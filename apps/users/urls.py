__author__ = "GodSuperK"
__date__ = "18-10-25 上午8:48"

from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views

app_name = "user"
urlpatterns = [

    path('login/', views.LoginView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('active/<str:code>/', views.ActiveUserView.as_view(), name="active"),
    path('forgetpwd/', views.ForgetPwdView.as_view(), name="forgetpwd"),
    path('pwd_reset/', views.PasswordResetView.as_view(), name="pwdreset"),
    path('uc/profile/', views.UserProfileView.as_view(), name="profile"),
    path('uc/modified_pwd/', views.PasswordModifiedView.as_view(), name="modified_pwd"),
    path('uc/my_course/', TemplateView.as_view(template_name="usercenter-mycourse.html"), name="my_course"),
    path('uc/message/', TemplateView.as_view(template_name="usercenter-message.html"), name="message"),
    path('uc/image/upload', views.UserImageUploadView.as_view(), name="upload_image"),

]
