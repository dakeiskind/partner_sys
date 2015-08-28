from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import generic
from django.views.decorators.http import require_GET
from material import LayoutMixin
from partner.models import Potential
from partner_sys import utils
from workflow.formal.models import FormalApprovalTask, FormalApprovalProcess

__author__ = 'chenqi'

from viewflow.views import StartProcessView
from viewflow import views as flow_views


class StartView(StartProcessView):

    def activation_done(self, *args, **kwargs):
        input = utils.load_json(self.request)
        potential_id = input['potential_id']
        try:
            potential = Potential.objects.get(id=potential_id)
        except Potential.DoesNotExist:
            potential = None

        if potential is None:
            return JsonResponse({'error':'指定的合作伙伴不存在'})

        self.process.created_by = self.request.user
        self.process.potential = potential
        self.done()


class AssignToView(flow_views.AssignView, generic.UpdateView):

    def post(self, request, *args, **kwargs):
        input = utils.load_json(self.request)
        task_id = input['task_id']
        assign_to = User.objects.get(id=input['assign_to'])

        if '_assign' or '_continue' in request.POST:
            self.assign(assign_to)
            # task_message_user(
            #     request, self.task,
            #     'assigned to {}'.format(request.user.get_full_name() or request.user.username))
            # return JsonResponse(r'{"info":"assigned to %(owner)s"}' % {'owner':assign_to.username})
            return JsonResponse({"info":"assigned to %s" % assign_to.username})
        else:
            return self.get(request, *args, **kwargs)


class ApproveView(flow_views.TaskViewMixin, generic.UpdateView):
    model = Potential
    fields = []

    def get_object(self):
        return self.activation.process.potential

    def activation_done(self, *args, **kwargs):
        self._approve()
        self.activation.done()

    def _approve(self):
        input = utils.load_json(self.request)

        self.activation.process.comment = input['proc_comment'].strip()
        if 'True' == input['is_approved']:
            self.activation.process.is_approved = True
        else:
            self.activation.process.is_approved = False
        self.activation.process.approver = self.request.user
        self.activation.process.save()

        if self.activation.process.is_approved is True:
            self.activation.process.potential.is_formal = True
            self.activation.process.potential.save()

        return self.activation.process


@require_GET
@login_required()
@user_passes_test(lambda u: u.is_superuser)
def no_mans_tasks(request):
    task_set = FormalApprovalTask.nomans.filter(flow_task='formal/flows.FormalApprovalFlow.approve')

    response_data = {}
    response_data['no_mans_tasks'] = task_data = []
    response_data['processes'] = process_data = {}
    for idx,task in enumerate(task_set):
        if 'DONE' != task.process.status:
            task_data.append({'task_id':task.id, 'process_id':task.process.id, 'created':task.created})
            process_data[task.process.id] = task.process.__dict__
            del process_data[task.process.id]['_state']
            del process_data[task.process.id]['flow_cls']

    return JsonResponse(response_data)


@require_GET
@login_required()
@user_passes_test(lambda u: u.is_superuser)
def all_tasks(request):
    task_set = FormalApprovalTask.objects.filter(flow_task='formal/flows.FormalApprovalFlow.approve')

    response_data = {}
    response_data['all_tasks'] = task_data = []
    response_data['processes'] = process_data = {}
    for idx,task in enumerate(task_set):
        if 'DONE' != task.process.status:
            task_data.append({'task_id':task.id, 'process_id':task.process.id, 'created':task.created})
            process_data[task.process.id] = task.process.__dict__
            del process_data[task.process.id]['_state']
            del process_data[task.process.id]['flow_cls']

    return JsonResponse(response_data)


@require_GET
@login_required()
def owned_tasks(request):
    task_set = FormalApprovalTask.objects.filter(owner=request.user, flow_task_type='HUMAN').exclude(status='DONE')

    response_data = {}
    response_data['owned_tasks'] = task_data = []
    response_data['processes'] = process_data = {}
    for idx,task in enumerate(task_set):
        from workflow.formal.flows import FormalApprovalFlow

        if FormalApprovalFlow == task.process.flow_cls:
            task_data.append({'task_id':task.id, 'process_id':task.process.id, 'created':task.created, 'flow_task':task.flow_task.name})
            process_data[task.process.id] = task.process.__dict__
            process_data[task.process.id]['potential_id'] = task.process.formalapprovalprocess.potential_id
            del process_data[task.process.id]['_state']
            del process_data[task.process.id]['flow_cls']
            del process_data[task.process.id]['_formalapprovalprocess_cache']

    return JsonResponse(response_data)



@require_GET
@login_required()
def my_created(request):
    processes = FormalApprovalProcess.objects.filter(created_by=request.user).exclude(status='DONE')

    response_data = {}
    response_data['my_proc'] = proc_data = []
    # response_data['processes'] = process_data = {}
    for idx, proc in enumerate(processes):
        proc_data.append(proc.__dict__)
        del proc_data[idx]['_state']
        del proc_data[idx]['flow_cls']

    return JsonResponse(response_data)


@require_GET
@login_required()
def proc_detail(request, process_pk):
    try:
        proc = FormalApprovalProcess.objects.get(id=process_pk).get(created_by=request.user)
    except FormalApprovalProcess.DoesNotExist:
        return JsonResponse({'error':u'找不到指定的流程实例'})

    if proc is not None:
        tasks = FormalApprovalTask.objects.filter(process=proc).order_by('created')

        response_data = {}
        response_data['tasks'] = task_data = []
        for t in tasks:
            if t.owner:
                owner = t.owner.username
            else:
                owner = None
            task_data.append({'task_id':t.id, 'flow_task':t.flow_task.name, 'status':t.status, 'finished':t.finished,
                              'owner':owner, 'process_id':t.process.id, 'comments':t.comments})
        response_data['proc'] = proc.__dict__
        del response_data['proc']['_state']
        del response_data['proc']['flow_cls']

        return JsonResponse(response_data)
    else:
        return JsonResponse({'error':u'找不到指定的流程实例'})
