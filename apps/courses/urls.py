__author__ = "GodSuperK"
__date__ = "18-10-22 下午1:46"

from django.urls import path
from . import views

app_name = "course"

urlpatterns = [
    path(r'list/', views.CourseListView.as_view(), name='list'),
    path(r'detail/<int:course_id>/', views.CourseDetailView.as_view(), name='detail'),
    path(r'detail/<int:course_id>/video/', views.CourseVideoView.as_view(), name='video'),
    path(r'detail/<int:course_id>/comment/', views.CourseCommentView.as_view(), name='comment'),
]
