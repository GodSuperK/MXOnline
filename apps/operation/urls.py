__author__ = "GodSuperK"
__date__ = "18-10-22 上午7:20"

from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "operation"
urlpatterns = [
    path('add_fav/', views.AddFavourite.as_view(), name="add_fav"),
]
