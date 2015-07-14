__author__ = 'chenqi'

from django.contrib import admin
from notice.models import *


class AnnouncementAdmin(admin.ModelAdmin):
    # list_display = ('creation_time', 'annouce_time', 'last_modified',)
    ordering = ('-creation_time', '-announce_time', '-last_modified')

admin.site.register(BiddingNotice, AnnouncementAdmin)
admin.site.register(BidNotice, AnnouncementAdmin)
admin.site.register(PriorNotice, AnnouncementAdmin)
admin.site.register(ChangeNotice, AnnouncementAdmin)
