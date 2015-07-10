__author__ = 'chenqi'

from django.conf.urls import patterns, url
import secur_auth.views as auth_views


urlpatterns = patterns('',
    url(r'^signin/$', auth_views.sign_in),
    url(r'^signup/$', auth_views.sign_up),
    url(r'^signout/$', auth_views.sign_out),
    url(r'^reset_pwd/$', auth_views.reset_pwd),
    )