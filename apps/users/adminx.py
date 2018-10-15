__author__ = "GodSuperK"
__date__ = "18-10-15 下午3:29"

from .models import EmailVerifyCode
from .models import Banner

import xadmin
from xadmin import views


class BaseSettings:
    enable_themes = True  # 启动切换主题功能
    use_bootswatch = True  # 添加bootstrap主题


class GlobalSettings:
    site_title = "GMOOC"  # 页面标题
    site_footer = "gmooc"  # 页面版权
    menu_style = "accordion"  # 折叠标签


xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)


class EmailVerifyCodeAdmin:
    # 自定义显示字段
    list_display = ['email', 'code', 'send_type', 'send_time']
    # 自定义搜索字段
    search_fields = ['email', 'code', 'send_type']
    # 自定义筛选字段
    list_filter = ['email', 'code', 'send_type', 'send_time']


class BannerAdmin:
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyCode, EmailVerifyCodeAdmin)
xadmin.site.register(Banner, BannerAdmin)
