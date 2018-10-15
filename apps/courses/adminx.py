__author__ = "GodSuperK"
__date__ = "18-10-15 下午4:09"

import xadmin

from .models import Course
from .models import Chapter
from .models import Video
from .models import CourseResource


class CourseAdmin:
    list_display = ['title', 'desc', 'degree', 'duration', 'nums_of_learning', 'hits', 'nums_of_staring', 'add_time']
    search_fields = ['title', 'degree', 'duration', 'hits', 'nums_of_staring']
    list_filter = ['title', 'degree', 'duration', 'nums_of_learning', 'hits', 'nums_of_staring', 'add_time']


class ChapterAdmin:
    list_display = ['course', 'title', 'add_time']
    search_fields = ['course', 'title']
    list_filter = ['course__title', 'title', 'add_time']


class VideoAdmin:
    list_display = ['chapter', 'title', 'add_time']
    search_fields = ['chapter', 'title']
    list_filter = ['chapter__title', 'title', 'add_time']


class CourseResourceAdmin:
    list_display = ['course', 'title', 'download', 'add_time']
    search_fields = ['course', 'title', 'download']
    list_filter = ['course__title', 'title', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Chapter, ChapterAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
