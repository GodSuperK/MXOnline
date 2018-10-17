__author__ = "GodSuperK"
__date__ = "18-10-17 上午9:37"

from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    # required=True, 表示该字段不可为空
    # min_length=4, 表示该字段最小长度4
    # 字段名称必须和表单字段的name值一样
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=4)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=8)
    captcha = CaptchaField() # error_message 可以自定义错误消息
