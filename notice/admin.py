__author__ = 'chenqi'

from django.contrib import admin
from notice.models import *
from common.admin import AnnouncementAdmin


admin.site.register(Bidding, AnnouncementAdmin)
admin.site.register(Bid, AnnouncementAdmin)
admin.site.register(Prior, AnnouncementAdmin)
admin.site.register(Change, AnnouncementAdmin)
