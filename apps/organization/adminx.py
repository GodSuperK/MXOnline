__author__ = "GodSuperK"
__date__ = "18-10-15 下午4:19"

import xadmin

from .models import CityDict
from .models import CourseOrg
from .models import Teacher


class CityDictAdmin:
    list_display = ['name', 'add_time']
    search_fields = ['name']
    list_filter = ['name', 'add_time']


class CourseOrgAdmin:
    list_display = ['name', 'desc', 'hits', 'nums_of_staring', 'address', 'city', 'add_time']
    search_fields = ['name', 'hits', 'nums_of_staring', 'address', 'city']
    list_filter = ['name', 'hits', 'nums_of_staring', 'address', 'city__name', 'add_time']


class TeacherAdmin:
    list_display = ['organization', 'name', 'working_experience', 'company', 'position', 'hits', 'nums_of_staring',
                    'add_time']
    search_fields = ['organization', 'name', 'working_experience', 'company', 'position', 'hits', 'nums_of_staring',
                     ]
    list_filter = ['organization__name', 'name', 'working_experience', 'company', 'position', 'hits', 'nums_of_staring',
                   'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
