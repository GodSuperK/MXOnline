from datetime import datetime

from django.db import models


# Create your models here.

class CityDict(models.Model):
    """城市信息模型"""
    name = models.CharField(verbose_name="城市名称", max_length=20)
    # 为后期扩展考虑，可能用不到该描述字段
    desc = models.CharField(verbose_name="城市描述", max_length=200)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "城市信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    """课程机构信息模型"""
    name = models.CharField(verbose_name="机构名称", max_length=30)
    desc = models.TextField(verbose_name="机构描述")
    category = models.IntegerField(verbose_name="机构类别", choices=((1, '培训机构'), (2, '高校'), (3, '个人')), default=2)
    hits = models.IntegerField(verbose_name="点击数", default=0)
    nums_of_staring = models.IntegerField(verbose_name="收藏数", default=0)
    image = models.ImageField(verbose_name="Logo", upload_to="organization/%Y/%m", max_length=200, blank=True)
    address = models.CharField(verbose_name="机构地址", max_length=200)
    # 根据城市筛选机构
    city = models.ForeignKey(verbose_name="城市", to=CityDict, on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "课程机构信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """机构教师基本信息模型"""
    organization = models.ForeignKey(verbose_name="所属机构", to=CourseOrg, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="教师姓名", max_length=20)
    working_experience = models.IntegerField(verbose_name="工作经验", default=0)
    company = models.CharField(verbose_name="公司", max_length=50)
    position = models.CharField(verbose_name="职位", max_length=50)
    features_of_teaching = models.CharField(verbose_name="教学特点", max_length=50)
    hits = models.IntegerField(verbose_name="点击数", default=0)
    nums_of_staring = models.IntegerField(verbose_name="收藏人数", default=0)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "机构教师信息"
        verbose_name_plural = verbose_name
