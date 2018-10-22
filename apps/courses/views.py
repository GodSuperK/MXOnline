from django.shortcuts import render
from django.views.generic import View
from utils.common import has_star
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import Course


# Create your views here.

class CourseListView(View):

    def get(self, request):
        # 默认按最新排序
        all_courses = Course.objects.all().order_by('-add_time')
        # 按最热门（点击数）,学习人数排序
        sort = request.GET.get('sort', '')
        if sort in ['hits', 'nums_of_learning']:
            all_courses = all_courses.order_by("-{}".format(sort))

        # 右侧显示3个热门课程
        hot_courses = Course.objects.all().order_by('-hits')[:3]
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, request=request, per_page=9)
        all_courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': all_courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


class CourseDetailView(View):

    def get(self, request, course_id):
        course = Course.objects.filter(id=course_id).first()
        # 收藏判断
        is_course_star = has_star(request.user, course.id, 1)
        is_org_star = has_star(request.user, course.org_id, 3)

        relate_course = None
        if course.tag:
            relate_course = [i for i in Course.objects.filter(tag=course.tag) if i.id != course_id][0]
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_course': relate_course,
            'is_course_star': is_course_star,
            'is_org_star': is_org_star
        })
