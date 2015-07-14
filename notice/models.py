__author__ = 'chenqi'

from django.db import models
from common.models import Announcement

class BiddingNotice(Announcement):
    pass

class BidNotice(Announcement):
    pass

class PriorNotice(Announcement):
    pass

class ChangeNotice(Announcement):
    pass