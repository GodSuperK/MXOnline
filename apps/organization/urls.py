__author__ = "GodSuperK"
__date__ = "18-10-20 上午9:42"

from django.urls import path
from . import views

app_name = "organization"
urlpatterns = [
    path('list/', views.OrgListView.as_view(), name="list"),
    path('add_ask/', views.UserAskView.as_view(), name="add_ask"),
]
