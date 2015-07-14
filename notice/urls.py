__author__ = 'chenqi'

from django.conf.urls import patterns, url
import notice.views as notice_views


urlpatterns = patterns('',
    url(r'^bidding/list/(?P<page>\d+)/(?P<size>\d+)/$', notice_views.list_bidding),
    url(r'^bid/list/(?P<page>\d+)/(?P<size>\d+)/$', notice_views.list_bid),
    url(r'^prior/list/(?P<page>\d+)/(?P<size>\d+)/$', notice_views.list_prior),
    url(r'^change/list/(?P<page>\d+)/(?P<size>\d+)/$', notice_views.list_change),
    )