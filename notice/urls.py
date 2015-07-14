__author__ = 'chenqi'

from django.conf.urls import patterns, url
import notice.views as notice_views


urlpatterns = patterns('',
    url(r'^bidding/today/$', notice_views.bidding_today),
    url(r'^bid/today/$', notice_views.bid_today),
    url(r'^prior/today/$', notice_views.prior_today),
    url(r'^change/today/$', notice_views.change_today),
    )