from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger

from .models import CourseOrg
from .models import CityDict
from .models import Teacher
from .forms import UserAskModelForm
from utils.common import has_star
import json


# Create your views here.

class OrgListView(generic.View):

    def get(self, request):

        # 热门机构根据收藏人数排序，显示3个机构
        hot_orgs = CourseOrg.objects.order_by("-hits")[:3]
        # 显示已有城市
        cities = CityDict.objects.all()

        # 获取所有查询参数
        ct = request.GET.get('ct', '')
        city_id = request.GET.get('city', '')
        # 获取排序参数
        sort = request.GET.get('sort', '')
        # 查询所有机构
        all_orgs = CourseOrg.objects.all()

        # 关键词搜索
        keywords = request.GET.get('keywords', '')
        if keywords:
            # 搜索name, desc, 将包含关键词的机构全部显示出来
            all_orgs = all_orgs.filter(
                Q(name__icontains=keywords) |
                Q(desc__icontains=keywords))

        # 机构筛选 by 机构类别(category)
        if ct:
            all_orgs = all_orgs.filter(category=int(ct))
        # 机构筛选 by 城市(city_id)
        if city_id:
            # CourseOrg 中的city 外键在数据表中存储为 city_id
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 机构数量
        nums_org = all_orgs.count()
        if sort in ['nums_of_students', 'nums_of_courses']:
            # 排序 by 学习人数(nums_of_students)或课程数(nums_of_courses)
            all_orgs = all_orgs.order_by("-{}".format(sort))

        # 对机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # per_page 表示每页显示的记录条数
        p = Paginator(all_orgs, request=request, per_page=5)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'orgs': orgs,
            'cities': cities,
            'nums_org': nums_org,
            'city_id': city_id,
            'ct': ct,
            'sort': sort,
            'hot_orgs': hot_orgs,
        })

    def post(self, request):
        pass


class UserAskView(generic.View):
    """用户咨询View
    该功能客户端使用ajax发送异步请求，
    当用户点击提交按钮后，页面不能刷新, 我们需要返回json格式的数据
    """

    def post(self, request):
        # 定义返回的json数据
        result = dict()
        user_ask_form = UserAskModelForm(request.POST)
        if user_ask_form.is_valid():
            # 使用表单的快捷方式save 来对模型进行快速实例化，并保存到数据库中
            user_ask_form.save(commit=True)
            result["status"] = "success"
            # 告诉浏览器，我们返回的是json数据, 让浏览器交给 ajax 去解析
            return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            result["status"] = "failed"
            result["error"] = "添加出错"
            return HttpResponse(json.dumps(result), content_type="application/json")


class OrgDetailView(generic.View):

    def get(self, request, org_id):
        # 查询机构
        org = CourseOrg.objects.filter(id=org_id).first()
        # 点击数加1
        org.hits += 1
        org.save()
        # 机构首页课程， 使用机构进行反向查询
        all_courses = org.course_set.all()[:3]
        # 显示3个教师
        all_teachers = org.teacher_set.all()[:3]

        return render(request,
                      'org-detail-homepage.html', {
                          'course_org': org,
                          'all_courses': all_courses,
                          'all_teachers': all_teachers,
                          'current_page': 'home',
                          # 是否已收藏
                          'has_star': has_star(request.user, fav_id=org_id, fav_type=3)
                      })


class OrgCourseView(generic.View):

    def get(self, request, org_id):
        org = CourseOrg.objects.filter(id=org_id).first()
        all_courses = org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'course_org': org,
            'all_courses': all_courses,
            'current_page': 'course',
            'has_star': has_star(request.user, fav_id=org_id, fav_type=3)
        })


class OrgDescView(generic.View):

    def get(self, request, org_id):
        org = CourseOrg.objects.filter(id=org_id).first()

        return render(request, 'org-detail-desc.html', {
            'course_org': org,
            'current_page': 'desc',
            'has_star': has_star(request.user, fav_id=org_id, fav_type=3)
        })


class OrgTeacherView(generic.View):

    def get(self, request, org_id):
        org = CourseOrg.objects.filter(id=org_id).first()
        all_teachers = org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'course_org': org,
            'all_teachers': all_teachers,
            'current_page': 'teacher',
            'has_star': has_star(request.user, fav_id=org_id, fav_type=3)
        })


class TeacherListView(generic.View):

    def get(self, request):
        # 默认根据收藏数进行排序
        teachers = Teacher.objects.order_by("-nums_of_staring").all()

        # 关键词搜索
        keywords = request.GET.get('keywords', '')
        if keywords:
            # 搜索教师姓名, 机构名字 将包含关键词的老师全部显示出来
            teachers = teachers.filter(
                Q(name__icontains=keywords) |
                Q(organization__name__icontains=keywords))

        sort = request.GET.get('sort', '')
        # 根据点击数进行排序
        if sort in ['hot', ]:
            teachers = teachers.order_by('-hits').all()

        # 讲师数量
        nums_of_teacher = teachers.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # per_page 表示每页显示的记录条数
        p = Paginator(teachers, request=request, per_page=3)

        all_teacher = p.page(page)

        # 讲师排行榜，根据点击数进行排序
        hot_teachers = teachers.order_by('-hits').all()[:3]

        return render(request, 'teachers-list.html', {
            'all_teacher': all_teacher,
            'nums_of_teacher': nums_of_teacher,
            'sort': sort,
            "hot_teachers": hot_teachers,

        })


class TeacherDetailView(generic.View):

    def get(self, request, teacher_id):
        teacher = Teacher.objects.filter(id=teacher_id).first()

        # 查询是否已收藏
        has_teacher_star = has_star(request.user, fav_id=teacher_id, fav_type=2)
        has_org_star = has_star(request.user, fav_id=teacher.organization_id, fav_type=3)

        # 讲师排行榜，根据点击数进行排序
        hot_teachers = Teacher.objects.all().order_by('-hits')[:3]
        return render(request, 'teacher-detail.html', {
            "teacher": teacher,
            'hot_teachers': hot_teachers,
            'has_teacher_star': has_teacher_star,
            'has_org_star': has_org_star,
        })
