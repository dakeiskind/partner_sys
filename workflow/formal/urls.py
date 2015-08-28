from viewflow import views as viewflow
from workflow.formal import views
from workflow.formal.flows import FormalApprovalFlow

from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    url(r'^', include([
        FormalApprovalFlow.instance.urls,
        url('^$', viewflow.ProcessListView.as_view(), name='index'),
        url('^tasks/$', viewflow.TaskListView.as_view(), name='tasks'),
        url('^queue/$', viewflow.QueueListView.as_view(), name='queue'),
        url('^details/(?P<process_pk>\d+)/$', viewflow.ProcessDetailView.as_view(), name='details'),
    ], namespace=FormalApprovalFlow.instance.namespace), {'flow_cls': FormalApprovalFlow}),
    url(r'^no_mans_tasks/$', views.no_mans_tasks),
    url(r'^all_tasks/$', views.no_mans_tasks),
    url(r'^owned_tasks/$', views.owned_tasks),
    url(r'^my_created/$', views.my_created),
    url(r'^proc_detail/(?P<process_pk>\d+)/$', views.proc_detail),
)
