from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

import json
from .models import UserStar


# Create your views here.

class AddFavourite(generic.View):

    def get(self, request):
        result = dict()
        # 取出异步请求提交的参数
        fav_id = request.GET.get('fav_id')
        fav_type = request.GET.get('fav_type')
        # 判断用户是否登陆
        if request.user.is_authenticated:
            # 判断参数是否合法
            if fav_id and fav_type:
                is_existed = UserStar.objects.filter(id_of_staring=fav_id, type_of_staring=fav_type)
                # 数据库存在记录，则取消收藏
                if is_existed:
                    is_existed.delete()
                    result["status"] = "success"
                    result["msg"] = "收藏"
                    return HttpResponse(json.dumps(result), content_type="application/json")
                # 数据库不存在记录，则添加收藏
                UserStar(
                    user=request.user,
                    id_of_staring=fav_id,
                    type_of_staring=fav_type).save()
                result["status"] = "success"
                result["msg"] = "已收藏"
                return HttpResponse(json.dumps(result), content_type="application/json")

            else:
                result["status"] = "fail"
                result["msg"] = "收藏出错"
                return HttpResponse(json.dumps(result), content_type="application/json")
        else:
            result["status"] = "fail"
            result["msg"] = "用户未登陆"
            return HttpResponse(json.dumps(result), content_type="application/json")
