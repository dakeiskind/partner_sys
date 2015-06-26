from django.conf.urls import patterns, url, include
from viewflow import views as viewflow
from hello_to_viewflow.flows import HelloWorldFlow
from hello_to_viewflow.views import *
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^helloworld/', include([
        HelloWorldFlow.instance.urls,
        url('^$', viewflow.ProcessListView.as_view(), name='index'),
        url('^tasks/$', viewflow.TaskListView.as_view(), name='tasks'),
        url('^queue/$', viewflow.QueueListView.as_view(), name='queue'),
        url('^details/(?P<process_pk>\d+)/$', viewflow.ProcessDetailView.as_view(), name='details'),
    ], namespace=HelloWorldFlow.instance.namespace), {'flow_cls': HelloWorldFlow}))