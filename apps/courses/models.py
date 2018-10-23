from datetime import datetime

from django.db import models
from organization.models import CourseOrg
from organization.models import Teacher


# Create your models here.

class Course(models.Model):
    """
    课程基本信息模型
    """
    title = models.CharField(verbose_name="课程名", max_length=50)
    desc = models.CharField(verbose_name="课程描述", max_length=300)
    teacher = models.ForeignKey(verbose_name="讲师", to=Teacher, on_delete=models.CASCADE, null=True, blank=True)
    # 课程详情使用富文本编辑
    detail = models.TextField(verbose_name="课程详情")
    # 课程公告
    notice = models.CharField(verbose_name="课程公告", max_length=100, blank=True, null=True)
    degree = models.CharField(verbose_name="课程难度",
                              choices=(('beginning', '初级'), ('intermediate', '中级'), ('advance', "高级")),
                              max_length=12,
                              default='intermediate')
    category = models.CharField(verbose_name="课程类别", max_length=20, blank=True, null=True)
    # TODO 进行外键关联
    tag = models.CharField(verbose_name="标签", max_length=10, null=True, blank=True)
    duration = models.IntegerField(verbose_name="学习时长(分钟数)", default=0)
    org = models.ForeignKey(verbose_name="所属机构", to=CourseOrg, on_delete=models.CASCADE, null=True, blank=True)
    nums_of_learning = models.IntegerField(verbose_name="学习人数", default=0)
    image = models.ImageField(verbose_name="课程封面", upload_to="courses/image/%Y/%m", max_length=100, blank=True)
    hits = models.IntegerField(verbose_name="点击数", default=0)
    nums_of_staring = models.IntegerField(verbose_name="收藏人数", default=0)
    need_know = models.CharField(verbose_name="课程须知", max_length=100, null=True, blank=True)
    learn_what = models.CharField(verbose_name="具体内容", max_length=300, null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "课程基本信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_chapter_nums(self):
        return self.chapter_set.all().count()

    def get_chapters(self):
        return self.chapter_set.all()

    def get_students(self):
        """return UserCourse QuerySet"""
        return self.usercourse_set.all()[:5]

    def get_resource(self):
        return self.courseresource_set.all()


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
        return "{}:{}".format(self.course.title, self.title)

    def get_video(self):
        return self.video_set.all()


class Video(models.Model):
    """
    章节的视频资源
    """
    chapter = models.ForeignKey(verbose_name="章节", to=Chapter, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="视频名", max_length=100)
    url = models.CharField(verbose_name="视频地址", max_length=200, null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    # url = models.URLField(verbose_name="播放地址", max_length=300)

    class Meta:
        verbose_name = "章节视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


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

    def __str__(self):
        return self.title

