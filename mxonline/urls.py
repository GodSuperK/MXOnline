"""mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin
from users import views as users_views
from mxonline.settings import MEDIA_ROOT

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    # 配置首页, name 参数在模板中的使用 {% url 'name' %}
    path('', TemplateView.as_view(template_name="index.html"), name="index"),
    path('login/', users_views.LoginView.as_view(), name="login"),
    path('register/', users_views.RegisterView.as_view(), name="register"),
    path('captcha/', include('captcha.urls')),
    re_path(r'^active/(?P<code>\w+)/$', users_views.ActiveUserView.as_view(), name="active"),
    path('forgetpwd/', users_views.ForgetPwdView.as_view(), name="forgetpwd"),
    path('pwd_reset/', users_views.PasswordResetView.as_view(), name="pwdreset"),
    # 课程机构首页
    path('org/', include('organization.urls')),
    path('operate/', include("operation.urls")),
    re_path(r'^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),

    path('course/', include('courses.urls')),
]
