from datetime import datetime

from django.db import models

from organization.models import CourseOrg


# Create your models here.

class Course(models.Model):
    """
    课程基本信息模型
    """
    title = models.CharField(verbose_name="课程名", max_length=50)
    desc = models.CharField(verbose_name="课程描述", max_length=300)
    # 课程详情使用富文本编辑
    detail = models.TextField(verbose_name="课程详情")
    degree = models.CharField(verbose_name="课程难度",
                              choices=(('beginning', '初级'), ('intermediate', '中级'), ('advance', "高级")),
                              max_length=12,
                              default='intermediate')
    duration = models.IntegerField(verbose_name="学习时长(分钟数)", default=0)
    org = models.ForeignKey(verbose_name="所属机构", to=CourseOrg, on_delete=models.CASCADE, null=True, blank=True)
    nums_of_learning = models.IntegerField(verbose_name="学习人数", default=0)
    image = models.ImageField(verbose_name="课程封面", upload_to="courses/image/%Y/%m", max_length=100)
    hits = models.IntegerField(verbose_name="点击数", default=0)
    nums_of_staring = models.IntegerField(verbose_name="收藏人数", default=0)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "课程基本信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Chapter(models.Model):
    """
    课程的章节模型
    """
    course = models.ForeignKey(verbose_name="课程", to=Course, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="章节名", max_length=100)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "课程章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Video(models.Model):
    """
    章节的视频资源
    """
    chapter = models.ForeignKey(verbose_name="章节", to=Chapter, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="视频名", max_length=100)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    # url = models.URLField(verbose_name="播放地址", max_length=300)

    class Meta:
        verbose_name = "章节视频"
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    """
    课程的其他资料
    """
    course = models.ForeignKey(verbose_name="课程", to=Course, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="资料名称", max_length=50)
    download = models.FileField(verbose_name="资源文件", upload_to="courses/resource/%Y/%m", max_length=200)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name
