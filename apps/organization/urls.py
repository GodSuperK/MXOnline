__author__ = "GodSuperK"
__date__ = "18-10-20 上午9:42"

from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "organization"
urlpatterns = [
    path('list/', views.OrgListView.as_view(), name="list"),
    path('add_ask/', views.UserAskView.as_view(), name="add_ask"),
    path('home/<int:org_id>/', views.OrgDetailView.as_view(), name="home"),
    path('course/<int:org_id>/', views.OrgCourseView.as_view(), name="course"),
    path('desc/<int:org_id>/', views.OrgDescView.as_view(), name="desc"),
    path('teacher/<int:org_id>/', views.OrgTeacherView.as_view(), name="teacher"),
]
