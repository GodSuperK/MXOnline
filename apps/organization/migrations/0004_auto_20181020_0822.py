# Generated by Django 2.1.2 on 2018-10-20 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20181019_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='nums_of_courses',
            field=models.IntegerField(default=0, verbose_name='课程数'),
        ),
        migrations.AddField(
            model_name='courseorg',
            name='nums_of_students',
            field=models.IntegerField(default=0, verbose_name='学习人数'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='image',
            field=models.ImageField(blank=True, max_length=200, upload_to='organization/%Y/%m', verbose_name='Logo'),
        ),
    ]
