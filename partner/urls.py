__author__ = 'Administrator'

from django.conf.urls import url
from partner import views
from partner import testUpload

urlpatterns = [
    url(r'^potentials/$', views.list_potentials),
    url(r'^potential/(?P<pid>\d+)/$', views.get_potential),
    url(r'^search/$', views.search),
    url(r'^potential/search/$', views.query_potentials),
    url(r'^potential/toupload/$', testUpload.toUpload),
    url(r'^potential/upload/$', testUpload.testUpload),
]