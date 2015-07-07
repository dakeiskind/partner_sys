__author__ = 'chenqi'

from django.contrib import admin
from common.models import Announcement


class AnnouncementAdmin(admin.ModelAdmin):
    # list_display = ('creation_time', 'annouce_time', 'last_modified',)
    ordering = ('-creation_time', '-announce_time', '-last_modified')

admin.site.register(Announcement, AnnouncementAdmin)
