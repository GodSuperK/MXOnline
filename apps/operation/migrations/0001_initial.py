# Generated by Django 2.1.2 on 2018-10-13 05:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=300, verbose_name='评论内容')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='评论时间')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='课程')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '课程评论',
                'verbose_name_plural': '课程评论',
            },
        ),
        migrations.CreateModel(
            name='UserAsk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='姓名')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('course_name', models.CharField(max_length=50, verbose_name='课程名')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '用户咨询',
                'verbose_name_plural': '用户咨询',
            },
        ),
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='开始学习')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='课程')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户已学习课程',
                'verbose_name_plural': '用户已学习课程',
            },
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(default=0, verbose_name='接收用户ID')),
                ('message', models.CharField(max_length=200, verbose_name='消息内容')),
                ('is_read', models.BooleanField(default=False, verbose_name='是否以读')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='发送时间')),
            ],
            options={
                'verbose_name': '用户消息',
                'verbose_name_plural': '用户消息',
            },
        ),
        migrations.CreateModel(
            name='UserStar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_of_staring', models.IntegerField(default=0, verbose_name='收藏对象的ID')),
                ('type_of_staring', models.IntegerField(choices=[(1, '课程'), (2, '教师'), (3, '机构')], default=1, verbose_name='收藏对象的类型')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='收藏时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户收藏',
                'verbose_name_plural': '用户收藏',
            },
        ),
    ]