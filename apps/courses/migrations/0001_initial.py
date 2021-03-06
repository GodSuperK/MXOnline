# Generated by Django 2.1.2 on 2018-10-13 05:34

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='章节名')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '课程章节',
                'verbose_name_plural': '课程章节',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='课程名')),
                ('desc', models.CharField(max_length=300, verbose_name='课程描述')),
                ('detail', models.TextField(verbose_name='课程详情')),
                ('degree', models.CharField(choices=[('beginning', '初级'), ('intermediate', '中级'), ('advance', '高级')], default='intermediate', max_length=12, verbose_name='课程难度')),
                ('duration', models.IntegerField(default=0, verbose_name='学习时长(分钟数)')),
                ('nums_of_learning', models.IntegerField(default=0, verbose_name='学习人数')),
                ('image', models.ImageField(upload_to='courses/image/%Y/%m', verbose_name='课程封面')),
                ('hits', models.IntegerField(default=0, verbose_name='点击数')),
                ('nums_of_staring', models.IntegerField(default=0, verbose_name='收藏人数')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '课程基本信息',
                'verbose_name_plural': '课程基本信息',
            },
        ),
        migrations.CreateModel(
            name='CourseResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='资料名称')),
                ('download', models.FileField(max_length=200, upload_to='courses/resource/%Y/%m', verbose_name='资源文件')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='课程')),
            ],
            options={
                'verbose_name': '课程资源',
                'verbose_name_plural': '课程资源',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='视频名')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Chapter', verbose_name='章节')),
            ],
            options={
                'verbose_name': '章节视频',
                'verbose_name_plural': '章节视频',
            },
        ),
        migrations.AddField(
            model_name='chapter',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='课程'),
        ),
    ]
