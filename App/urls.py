from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from App import views

urlpatterns = [
    url(r'^server/log/$', views.Find_in_databaseList.as_view()),
    url(r'^server/log/(?)/$', views.Find_in_databaseDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
