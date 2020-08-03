from django.urls import re_path
from src.co2_consumption.views import IndexView

urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name='index'),
]