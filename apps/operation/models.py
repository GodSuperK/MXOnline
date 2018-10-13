from datetime import datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course


# Create your models here.

class UserAsk(models.Model):
    """用户咨询模型"""
    name = models.CharField(verbose_name="姓名", max_length=20)
    phone = models.CharField(verbose_name="手机号", max_length=11)
    course_name = models.CharField(verbose_name="课程名", max_length=50)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name


class CourseComment(models.Model):
    """课程评论模型"""
    user = models.ForeignKey(verbose_name="用户", to=UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(verbose_name="课程", to=Course, on_delete=models.CASCADE)
    comment = models.CharField(verbose_name="评论内容", max_length=300)
    add_time = models.DateTimeField(verbose_name="评论时间", default=datetime.now)

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name


class UserStar(models.Model):
    """用户收藏模型"""
    user = models.ForeignKey(verbose_name="用户", to=UserProfile, on_delete=models.CASCADE)
    id_of_staring = models.IntegerField("收藏对象的ID", default=0)
    type_of_staring = models.IntegerField("收藏对象的类型", choices=((1, "课程"), (2, "教师"), (3, "机构")), default=1)
    add_time = models.DateTimeField(verbose_name="收藏时间", default=datetime.now)

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    """用户消息模型"""
    # 0 表示发送给所有用户
    user = models.IntegerField(verbose_name="接收用户ID", default=0)
    message = models.CharField(verbose_name="消息内容", max_length=200)
    is_read = models.BooleanField(verbose_name="是否以读", default=False)
    add_time = models.DateTimeField(verbose_name="发送时间", default=datetime.now)

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    """用户已学习课程模型"""
    user = models.ForeignKey(verbose_name="用户", to=UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(verbose_name="课程", to=Course, on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name="开始学习", default=datetime.now)

    class Meta:
        verbose_name = "用户已学习课程"
        verbose_name_plural = verbose_name
