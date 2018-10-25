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
    # 配置首页
    path('', users_views.IndexView.as_view(), name="index"),
    # 用户相关配置
    path('user/', include("users.urls")),
    # 机构配置
    path('org/', include('organization.urls')),
    # 课程配置
    path('course/', include('courses.urls')),
    # 用户操作配置
    path('operate/', include("operation.urls")),

    # xAdmin 后台管理系统配置
    path('xadmin/', xadmin.site.urls),
    # 上传文件处理函数
    # path('media/<str:path>/', serve, {'document_root': MEDIA_ROOT}),
    re_path(r'^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),
    # 验证码插件配置
    path('captcha/', include('captcha.urls')),
    # path('admin/', admin.site.urls), # Admin 后台管理系统配置
]
