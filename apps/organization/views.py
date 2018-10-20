from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views import generic
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg
from .models import CityDict


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
            'hot_orgs': hot_orgs
        })

    def post(self, request):
        pass
