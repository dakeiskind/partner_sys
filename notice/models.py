__author__ = 'chenqi'

from django.db import models
from common.models import Announcement

class BiddingNotice(Announcement):
    pass

class Bid(Announcement):
    pass

class Prior(Announcement):
    pass

class Change(Announcement):
    pass