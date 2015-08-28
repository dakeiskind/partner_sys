from viewflow import flow, lock
from viewflow.base import this, Flow

from workflow.formal import models as formal_models
from workflow.formal.views import StartView, ApproveView, AssignToView


class FormalApprovalFlow(Flow):
    process_cls = formal_models.FormalApprovalProcess
    task_cls = formal_models.FormalApprovalTask
    lock_impl = lock.select_for_update_lock

    start = flow.Start(StartView).Next(this.approve)

    approve = flow.View(ApproveView, assign_view=AssignToView.as_view()).Next(this.check_approve)

    check_approve = flow.If(cond=lambda p: p.is_approved) \
        .OnTrue(this.end).OnFalse(this.end)

    end = flow.End()