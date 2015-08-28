from django.conf.urls import patterns, url, include
from viewflow import views as viewflow
from django.contrib import admin
from django.conf import settings
from shipment.flows import ShipmentFlow

from workflow.flows import HelloWorldFlow
from workflow.views import *

urlpatterns = patterns('',
    url(r'^$', index, {'home':'home.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^common/', include('common.urls')),
    url(r'^auth/', include('secur_auth.urls')),
    url(r'^notice/', include('notice.urls')),
    url(r'^partner/', include('partner.urls')),
    url(r'^flow/potential/', include('workflow.potential.urls')),
    url(r'^flow/formal/', include('workflow.formal.urls')),
    # url(r'^helloworld/', include([
    #     HelloWorldFlow.instance.urls,
    #     url('^$', viewflow.ProcessListView.as_view(), name='index'),
    #     url('^tasks/$', viewflow.TaskListView.as_view(), name='tasks'),
    #     url('^queue/$', viewflow.QueueListView.as_view(), name='queue'),
    #     url('^details/(?P<process_pk>\d+)/$', viewflow.ProcessDetailView.as_view(), name='details'),
    # ], namespace=HelloWorldFlow.instance.namespace), {'flow_cls': HelloWorldFlow}),
    url(r'^shipment/', include([
        ShipmentFlow.instance.urls,
        url('^$', viewflow.ProcessListView.as_view(), name='index'),
        url('^tasks/$', viewflow.TaskListView.as_view(), name='tasks'),
        url('^queue/$', viewflow.QueueListView.as_view(), name='queue'),
        url('^details/(?P<process_pk>\d+)/$', viewflow.ProcessDetailView.as_view(), name='details'),
    ], namespace=ShipmentFlow.instance.namespace), {'flow_cls': ShipmentFlow}),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^imgs/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),)


# urlpatterns += patterns(url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),)
              #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

