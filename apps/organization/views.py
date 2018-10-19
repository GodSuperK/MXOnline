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

        # TODO 筛选查询逻辑有待优化
        cities = CityDict.objects.all()
        all_orgs = None
        ct = request.GET.get('ct', '')
        city_id = request.GET.get('city', '')
        if ct and city_id:
            ct = int(ct)
            city_id = int(city_id)
            # CourseOrg 中的city 外键在数据表中存储为 city_id
            all_orgs = CourseOrg.objects.filter(category=ct, city_id=city_id)
        elif ct:
            ct = int(ct)
            all_orgs = CourseOrg.objects.filter(category=ct)
        elif city_id:
            city_id = int(city_id)
            all_orgs = CourseOrg.objects.filter(city_id=city_id)
        else:
            all_orgs = CourseOrg.objects.all()

        # 机构数量
        nums_org = all_orgs.count()

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
            'hot_orgs': hot_orgs
        })

    def post(self, request):
        pass
