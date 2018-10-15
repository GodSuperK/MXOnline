from datetime import datetime

from django.db import models

from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    """
    用户个人信息模型
    """
    nick_name = models.CharField(verbose_name="昵称", max_length=30, default='')
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(verbose_name="性别", max_length=6, choices=(('male', '男'), ('female', '女')), default='male')
    address = models.CharField(verbose_name="地址", max_length=100, default='')
    phone = models.CharField(verbose_name="电话", max_length=11, null=True, blank=True)
    # upload_to 表示图片上传路径
    image = models.ImageField(verbose_name="头像", upload_to="image/%Y/%m", default="image/default.png", max_length=200)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyCode(models.Model):
    """
    邮箱验证模型
    """
    code = models.CharField(verbose_name="验证码", max_length=20)
    email = models.EmailField(verbose_name="邮箱", max_length=100)
    send_type = models.CharField(verbose_name="类型", choices=(('register', '注册'), ('forget', '找回密码')), max_length=8)
    send_time = models.DateTimeField(verbose_name="发送时间", default=datetime.now)

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}({})".format(self.email, self.send_type)


class Banner(models.Model):
    """轮播图模型"""
    title = models.CharField(verbose_name="标题", max_length=100)
    image = models.ImageField(verbose_name="上传图片", upload_to="banner/%Y/%m", max_length=200)
    url = models.URLField(verbose_name="访问地址", max_length=200)
    # 轮播图显示顺序
    index = models.IntegerField(verbose_name="显示顺序", default=100)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
