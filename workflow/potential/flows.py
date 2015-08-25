from viewflow import flow, lock
from viewflow.base import this, Flow

from workflow.potential import models as potential_models
from workflow.potential.views import launch_func, fill_in, approve, FillInView, ApproveView, AssignToView


class RegistryApprovalFlow(Flow):
    process_cls = potential_models.PotentialApprovalProcess
    task_cls = potential_models.PotentialApprovalTask
    lock_impl = lock.select_for_update_lock

    start = flow.StartFunction(launch_func).Next(this.fill_in)

    fill_in = flow.View(FillInView).Next(this.approve).Assign(lambda p: p.created_by)

    # assign_to = flow.View(AssignToView).Next(this.approve)
        # .Assign(username='admin')

    approve = flow.View(ApproveView, assign_view=AssignToView.as_view()).Next(this.check_approve)

    check_approve = flow.If(cond=lambda p: p.is_approved) \
        .OnTrue(this.end) \
        .OnFalse(this.fill_in)

    end = flow.End()