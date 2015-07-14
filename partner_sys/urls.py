from django.conf.urls import patterns, url, include
from viewflow import views as viewflow
from hello_to_viewflow.flows import HelloWorldFlow
from hello_to_viewflow.views import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import common.views as common_views

urlpatterns = patterns('',
    url(r'^$', index, {'home':'home.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^common/', include('common.urls')),
    url(r'^auth/', include('secur_auth.urls')),
    url(r'^notice/', include('notice.urls')),
    url(r'^helloworld/', include([
        HelloWorldFlow.instance.urls,
        url('^$', viewflow.ProcessListView.as_view(), name='index'),
        url('^tasks/$', viewflow.TaskListView.as_view(), name='tasks'),
        url('^queue/$', viewflow.QueueListView.as_view(), name='queue'),
        url('^details/(?P<process_pk>\d+)/$', viewflow.ProcessDetailView.as_view(), name='details'),
    ], namespace=HelloWorldFlow.instance.namespace), {'flow_cls': HelloWorldFlow}),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^imgs/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),)


# urlpatterns += patterns(url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),)
              #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

