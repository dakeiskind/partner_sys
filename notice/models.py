__author__ = 'chenqi'

from django.db import models
from common.models import Notice


class Bidding(Notice):
    pass

class Bid(Notice):
    pass

class Prior(Notice):
    pass

class Change(Notice):
    pass