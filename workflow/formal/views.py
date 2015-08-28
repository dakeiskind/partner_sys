from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import generic
from material import LayoutMixin
from partner.models import Potential
from partner_sys import utils

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