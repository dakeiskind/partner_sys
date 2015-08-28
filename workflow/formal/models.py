__author__ = 'chenqi'

from django.db import models
from django.contrib.auth.models import User
from viewflow.models import Process, Task
from partner.models import Potential


class NoMansManager(models.Manager):
    def get_queryset(self):
        return super(NoMansManager, self).get_queryset().filter(status='NEW', owner=None)


class FormalApprovalProcess(Process):
    potential = models.ForeignKey(Potential, blank=True, null=True)
    created_by = models.ForeignKey(User, blank=True, null=True, related_name='formal_created_by')
    is_approved = models.BooleanField(default=False)
    comment = models.CharField(max_length=1024)
    approver = models.ForeignKey(User, blank=True, null=True, related_name='formal_approver')


class FormalApprovalTask(Task):
    class Meta:
        proxy = True
        ordering = ["-created", "-started"]
        get_latest_by = "created"

    objects = models.Manager()
    nomans = NoMansManager()
