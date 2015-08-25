from viewflow import views as viewflow
from workflow.potential.flows import RegistryApprovalFlow
from workflow.potential import views

from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^', include([
        # url(r'^fillin/$', fill_in),
        # url(r'^approve/(?P<flow_cls>\w+)/(?P<process_pk>\d+)/(?P<flow_task>\w+)/(?P<task_pk>\d+)$', approve),
        RegistryApprovalFlow.instance.urls,
        url('^$', viewflow.ProcessListView.as_view(), name='index'),
        url('^tasks/$', viewflow.TaskListView.as_view(), name='tasks'),
        url('^queue/$', viewflow.QueueListView.as_view(), name='queue'),
        url('^details/(?P<process_pk>\d+)/$', viewflow.ProcessDetailView.as_view(), name='details'),
    ], namespace=RegistryApprovalFlow.instance.namespace), {'flow_cls': RegistryApprovalFlow}),

    url(r'^no_mans_tasks/$', views.no_mans_tasks),
    url(r'^owned_tasks/$', views.owned_tasks),
    url(r'^my_created/$', views.my_created),
    url(r'^proc_detail/(?P<process_pk>\d+)/$', views.proc_detail),
)
