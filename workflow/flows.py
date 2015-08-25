from viewflow import flow, lock
from viewflow.base import this, Flow
from viewflow.contrib import celery
from viewflow.views import StartProcessView, ProcessView
from workflow import models, tasks


class HelloWorldFlow(Flow):
    process_cls = models.HelloWorldProcess
    lock_impl = lock.select_for_update_lock

    start = flow.Start(StartProcessView, fields=["text"]) \
        .Permission(auto_create=True) \
        .Next(this.approve)


    approve = flow.View(ProcessView, fields=["approved"]) \
        .Permission(auto_create=True) \
        .Next(this.check_approve)

    check_approve = flow.If(cond=lambda p: p.approved) \
        .OnTrue(this.send) \
        .OnFalse(this.end)

    send = celery.Job(tasks.send_hello_world_request) \
        .Next(this.end)

    end = flow.End()