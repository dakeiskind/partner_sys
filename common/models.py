__author__ = 'chenqi'

from django.db import models

class DraftManager(models.Manager):
    def get_queryset(self):
        return super(DraftManager, self).get_queryset().filter(is_draft=True)

class FormalManager(models.Manager):
    def get_queryset(self):
        return super(FormalManager, self).get_queryset().filter(is_draft=False)

class Announcement(models.Model):
    title = models.CharField(max_length=128)
    is_draft = models.BooleanField(default=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    announce_time = models.DateTimeField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    read_time = models.IntegerField(default=0)
    paper_path = models.FilePathField(path=r"/home/chenqi/code_store/pycharm/partner_sys/templates/prototype_static/notice.html", null=True, blank=True)

    class Meta:
        ordering = ["-announce_time", "-last_modified"]
        # db_table = "announcement"
        get_latest_by = "Announce_time"

    drafts = DraftManager()
    formals = FormalManager()

    def __str__(self):
        return self.title