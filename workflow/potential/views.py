import datetime
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.views import generic
from django.views.decorators.http import require_POST, require_GET
import extra_views
from viewflow.flow import flow_view
from viewflow import views as flow_views
from partner.models import Contact, Potential
from partner_sys import utils
from workflow.potential.models import PotentialApprovalProcess, PotentialApprovalTask


@require_POST
@login_required()
@transaction.atomic
# @flow_view()
def fill_in(request):
    input = utils.load_json(request)
    # contact = input['contact']
    # potential = input['potential']
    user_id = input['user_id']
    process_id = input['process_id']

    user = User.objects.get(id=user_id)
    if user is None:
        return JsonResponse({'error':r'尚未进行用户注册'})

    # process = PotentialApprovalProcess.objects.get(id=process_id)

    if False:
        c = Contact()
        c.name = 'contact_01'
        c.title = 'no title'
        c.tel = '110'
        c.mobile = '13800138000'
        c.idCard = 'mei you'
        c.email = '1@1.com'
        c.idCopy = 'ye mei you'
        # c.name = contact.name
        # c.title = contact.title
        # c.tel = contact.tel
        # c.mobile = contact.mobile
        # c.idCard = contact.idCard
        # c.email = contact.email
        # c.idCopy = contact.idCopy
        # print(utils.to_json(c))
        print(c.__dict__)
        # c.save()


        p = Potential()
        p.zh_name = u'供应商_01'
        p.en_name = 'partner_01'
        p.ceo = 'Whoever'
        p.scope = 'what?'
        p.founding = datetime.datetime.today()
        p.capital = 100000000000
        p.licence = '0101010101010'
        p.licenceCopy = 'mei you'
        p.tax = 'mei you'
        p.taxCopy = 'ye mei you'
        p.orgCode = '250'
        p.orgCodeCopy = 'mei you'
        p.employees = 3
        p.address = r'beijing'
        p.homepage = r'www.bjhjyd.gov.cn'
        p.tel = '62620202'
        p.fax = '66668888'
        p.post = u'北京市630信箱'
        p.summary = 'blahblahblah....'
        # p.zh_name = potential.zh_name
        # p.en_name = potential.en_name
        # p.ceo = potential.ceo
        # p.scope = potential.scope
        # p.founding = potential.founding
        # p.capital = potential.capital
        # p.licence = potential.license
        # p.licenceCopy = potential.licenceCopy
        # p.tax = potential.tax
        # p.taxCopy = potential.taxCopy
        # p.orgCode = potential.orgCode
        # p.orgCodeCopy = potential.orgCodeCopy
        # p.employees = potential.employees
        # p.address = potential.address
        # p.homepage = potential.homepage
        # p.tel = potential.tel
        # p.fax = potential.fax
        # p.post = potential.post
        # p.summary = potential.summary
        # p.contact = c
        p.user = user
        # print(utils.to_json(p))
        print(p.__dict__)
        # p.save()

        # RegistryApprovalFlow.fill_in.run()
        return JsonResponse({'contact':c.id, 'potential':p.id})

@require_POST
@login_required()
# @flow_view()
def approve(request, activation, flow_cls, process_pk, flow_task, task_pk):
    # RegistryApprovalFlow.approve.run()
    activation.assign(None)

    return JsonResponse()

def launch_func(activation, **kwargs):
    if kwargs['created_by'] is not None \
        and isinstance(kwargs['created_by'], User):

        activation.prepare()
        activation.process.created_by = kwargs['created_by']
        activation.done()

    return activation


# class StartView(flow_views.StartViewMixin,
#                 extra_views.NamedFormsetsMixin,
#                 extra_views.CreateWithInlinesView):
#     model = PotentialApprovalProcess
#
#     def activation_done(self, form, inlines):
#         self.object = form.save()
#         for formset in inlines:
#             formset.save()
#
#         self.activation.process.created_by = self.request.user
#         self.activation.process.shipment = self.object
#         self.activation.done()


class FillInView(flow_views.TaskViewMixin, generic.UpdateView):
    model = Potential
    fields = []

    def get_object(self):
        input = utils.load_json(self.request)
        contact = input['contact']
        potential = input['potential']
        user = self.request.user

        self.activation.process.potential = \
            self._save_potential(user=user, contact=contact, potential=potential)
        self.activation.process.save()

        return self.activation.process.potential

    def activation_done(self, *args, **kwargs):
        self.activation.done()

    def form_valid(self, *args, **kwargs):
        # super(TaskViewMixin, self).form_valid(*args, **kwargs)
        self.activation_done(*args, **kwargs)
        self.message_complete()
        return JsonResponse({'info':'success'})

    def _save_potential(self, user=None, contact=None, potential=None):
        if contact['id'] is None or '' == contact['id']:
            c = Contact()
        else:
            c = Contact.objects.get(id=contact['id'])
        c.name = contact['name']
        c.title = contact['title']
        c.tel = contact['tel']
        c.mobile = contact['mobile']
        c.idCard = contact['idCard']
        c.email = contact['email']
        c.idCopy = contact['idCopy']
        # print(c.__dict__)
        c.save()

        if potential['id'] is None or '' == potential['id']:
            p = Potential()
        else:
            p = Potential.objects.get(id=potential['id'])
        p.zh_name = potential['zh_name']
        p.en_name = potential['en_name']
        p.ceo = potential['ceo']
        p.scope = potential['scope']
        p.founding = potential['founding']
        p.capital = potential['capital']
        p.licence = potential['licence']
        p.licenceCopy = potential['licenceCopy']
        p.tax = potential['tax']
        p.taxCopy = potential['taxCopy']
        p.orgCode = potential['orgCode']
        p.orgCodeCopy = potential['orgCodeCopy']
        p.employees = potential['employees']
        p.address = potential['address']
        p.homepage = potential['homepage']
        p.tel = potential['tel']
        p.fax = potential['fax']
        p.post = potential['post']
        p.summary = potential['summary']
        p.is_active = False
        p.contact = c
        p.user = user
        # print(p.__dict__)
        p.save()

        return p


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
            self.activation.process.potential.is_active = True
            self.activation.process.potential.save()

        return self.activation.process


@require_GET
@login_required()
@user_passes_test(lambda u: u.is_superuser)
def no_mans_tasks(request):
    task_set = PotentialApprovalTask.nomans.filter(flow_task='potential/flows.RegistryApprovalFlow.approve')

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
def owned_tasks(request):
    task_set = PotentialApprovalTask.objects.filter(owner=request.user, flow_task_type='HUMAN').exclude(status='DONE')

    response_data = {}
    response_data['owned_tasks'] = task_data = []
    response_data['processes'] = process_data = {}
    for idx,task in enumerate(task_set):
        from workflow.potential.flows import RegistryApprovalFlow

        if RegistryApprovalFlow == task.process.flow_cls:
        # if isinstance(task.process.flow_cls, RegistryApprovalFlow):
        # if type(task.process) == PotentialApprovalProcess:
            task_data.append({'task_id':task.id, 'process_id':task.process.id, 'created':task.created, 'flow_task':task.flow_task.name})
            process_data[task.process.id] = task.process.__dict__
            process_data[task.process.id]['potential_id'] = task.process.potentialapprovalprocess.potential_id
            del process_data[task.process.id]['_state']
            del process_data[task.process.id]['flow_cls']
            del process_data[task.process.id]['_potentialapprovalprocess_cache']

    return JsonResponse(response_data)


@require_GET
@login_required()
def my_created(request):
    processes = PotentialApprovalProcess.objects.filter(created_by=request.user).exclude(status='DONE')

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
        proc = PotentialApprovalProcess.objects.get(id=process_pk).get(created_by=request.user)
    except PotentialApprovalProcess.DoesNotExist:
        return JsonResponse({'error':u'找不到指定的流程实例'})

    if proc is not None:
        tasks = PotentialApprovalTask.objects.filter(process=proc).order_by('created')

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


