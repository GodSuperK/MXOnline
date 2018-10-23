__author__ = "GodSuperK"
__date__ = "18-10-23 下午8:46"

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin:
    """
    继承自这个类的View 需要用户登陆才能访问，否则会自动跳转到登陆页面
    实现view 的登陆页面跳转
    """

    @method_decorator(login_required(login_url='/login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
