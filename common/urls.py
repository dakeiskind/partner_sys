__author__ = 'chenqi'

from django.conf.urls import patterns, url, include
import common.views as common_views


urlpatterns = patterns('',
    url(r'^anno/list/(?P<page>\d+)/(?P<size>\d+)/$', common_views.anno_list),
)