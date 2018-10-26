from django.shortcuts import render
from django.views.generic import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import Course
from .models import Video
from operation.models import CourseComment
from operation.models import UserCourse
from utils.mixin_utils import LoginRequiredMixin
from utils.common import has_star


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
        # 点击数加1
        course.hits += 1
        course.save()
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


class CourseVideoView(LoginRequiredMixin, View):
    """
    用户学习课程，需要用户登陆(继承自LoginRequiredMixin 帮我们自动实现未登陆跳转到登陆页面)
    当用户点击开始学习按钮后，将课程与用户关联，
    同时每次访问，检查是否已关联，避免重复插入记录

    该课的同学还学过：
    查询所有学习过该课程的用户，找出还有哪些课程，被这些用户学习过，
    推荐几个被学习最多的课程
    """

    def get(self, request, course_id):
        course = Course.objects.filter(id=course_id).first()

        # -------用户学习课程 [开始]-------
        is_exist = UserCourse.objects.filter(user_id=request.user.id, course_id=course_id).first()
        if not is_exist:
            record = UserCourse()
            record.user = request.user
            record.course = course
            record.save()
        # -------用户学习课程 [结束]-------

        # -------该课的同学还学过 [开始]-------
        # 1. 查询所有学习过该课程的用户id
        q = UserCourse.objects.filter(course_id=course_id).all()
        u_id = [user_course.user_id for user_course in q]
        # 2. 根据用户id 查询每个用户所学的课程id
        q = UserCourse.objects.filter(user_id__in=u_id).all()
        c_id = [user_course.course_id for user_course in q]
        # 3. 统计每个课程id出现的次数
        times = dict()
        for i in c_id:
            times[i] = times.get(i, 0) + 1
        print(times)
        # 4. 进行排序
        x = sorted(times.items(), key=lambda item: item[1], reverse=True)
        # 取出现次数最多的3个课程, 此处不会报错，如果3超出了边界，也不会报错
        relate_courses_id = [i[0] for i in x[:4] if i[0] != course_id]
        relate_courses = Course.objects.filter(id__in=relate_courses_id)
        # -------该课的同学还学过 [完成]-------

        return render(request, 'course-video.html', {
            "course": course,
            'relate_courses': relate_courses
        })


class CourseCommentView(LoginRequiredMixin, View):

    def get(self, request, course_id):
        course = Course.objects.filter(id=course_id).first()
        # 根据课程id筛选所有评论，按最新时间排序,
        # TODO 对评论进行分页
        all_comment = CourseComment.objects.filter(course_id=course_id).order_by("-add_time")

        # -------该课的同学还学过 [开始]-------
        # 1. 查询所有学习过该课程的用户id
        q = UserCourse.objects.filter(course_id=course_id).all()
        u_id = [user_course.user_id for user_course in q]
        # 2. 根据用户id 查询每个用户所学的课程id
        q = UserCourse.objects.filter(user_id__in=u_id).all()
        c_id = [user_course.course_id for user_course in q]
        # 3. 统计每个课程id出现的次数
        times = dict()
        for i in c_id:
            times[i] = times.get(i, 0) + 1
        print(times)
        # 4. 进行排序
        x = sorted(times.items(), key=lambda item: item[1], reverse=True)
        # 取出现次数最多的3个课程id, 此处不会报错，如果3超出了边界，也不会报错
        relate_courses_id = [i[0] for i in x[:4] if i[0] != course_id]
        relate_courses = Course.objects.filter(id__in=relate_courses_id)
        # -------该课的同学还学过 [完成]-------

        return render(request, 'course-comment.html', {
            "course": course,
            'all_comment': all_comment,
            'relate_courses': relate_courses
        })


class PlayVideoView(LoginRequiredMixin, View):
    def get(self, request, course_id, video_id):
        # 查询视频
        video = Video.objects.filter(id=video_id).first()

        course = Course.objects.filter(id=course_id).first()

        # -------该课的同学还学过 [开始]-------
        # 1. 查询所有学习过该课程的用户id
        q = UserCourse.objects.filter(course_id=course_id).all()
        u_id = [user_course.user_id for user_course in q]
        # 2. 根据用户id 查询每个用户所学的课程id
        q = UserCourse.objects.filter(user_id__in=u_id).all()
        c_id = [user_course.course_id for user_course in q]
        # 3. 统计每个课程id出现的次数
        times = dict()
        for i in c_id:
            times[i] = times.get(i, 0) + 1
        print(times)
        # 4. 进行排序
        x = sorted(times.items(), key=lambda item: item[1], reverse=True)
        # 取出现次数最多的3个课程, 此处不会报错，如果3超出了边界，也不会报错
        relate_courses_id = [i[0] for i in x[:4] if i[0] != course_id]
        relate_courses = Course.objects.filter(id__in=relate_courses_id)
        # -------该课的同学还学过 [完成]-------

        return render(request, 'course-play.html', {
            "course": course,
            'relate_courses': relate_courses,
            'video': video
        })
