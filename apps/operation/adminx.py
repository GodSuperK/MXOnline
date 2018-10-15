__author__ = "GodSuperK"
__date__ = "18-10-15 下午4:25"

import xadmin

from .models import UserAsk
from .models import CourseComment
from .models import UserStar
from .models import UserMessage
from .models import UserCourse


class UserAskAdmin:
    list_display = ['name', 'phone', 'course_name', 'add_time']
    search_fields = ['name', 'phone', 'course_name']
    list_filter = ['name', 'phone', 'course_name', 'add_time']


class CourseCommentAdmin:
    list_display = ["user", 'course', 'comment', 'add_time']
    search_fields = ["user", 'course', 'comment']
    list_filter = ["user__username", 'course', 'comment', 'add_time']


class UserStarAdmin:
    list_display = ['user', 'id_of_staring', 'type_of_staring', 'add_time']
    search_fields = ['user', 'id_of_staring', 'type_of_staring']
    list_filter = ['user__username', 'id_of_staring', 'type_of_staring', 'add_time']


class UserMessageAdmin:
    list_display = ['user', 'message', 'is_read', 'add_time']
    search_fields = ['user', 'message', 'is_read']
    list_filter = ['user__username', 'message', 'is_read', 'add_time']


class UserCourseAdmin:
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user__username', 'course', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComment, CourseCommentAdmin)
xadmin.site.register(UserStar, UserStarAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
