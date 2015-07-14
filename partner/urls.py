__author__ = 'Administrator'

from django.conf.urls import url
from partner import views


urlpatterns = [
    url(r'^potentials/$', views.list_potentials),
    url(r'^potential/(?P<pid>\d+)/$', views.get_potential),
    url(r'^search/$', views.search),
    url(r'^potential/search/$', views.query_potentials),
]