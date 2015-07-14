__author__ = 'chenqi'

from django.http import HttpRequest, HttpResponse, Http404, JsonResponse
from django.views.decorators.http import *
from django.db.models import Q
from notice.models import *
import datetime

@require_GET
def bidding_today(request):
    res_data = __notice_today(Bidding, r'../imgs/icon1.png', u'招标公告')
    return JsonResponse(res_data)

@require_GET
def bid_today(request):
    res_data = __notice_today(Bid, r'../imgs/icon2.png', u'中标公告')
    return JsonResponse(res_data)

@require_GET
def prior_today(request):
    res_data = __notice_today(Prior, r'../imgs/icon3.png', u'招标预告')
    return JsonResponse(res_data)

@require_GET
def change_today(request):
    res_data = __notice_today(Change, r'../imgs/icon4.png', u'变标公告')
    return JsonResponse(res_data)

def __notice_today(notice_type, icon=r'../imgs/icon1.png', title=u'公告'):
    notice_types = [Bidding, Bid, Prior, Change]
    if notice_type in notice_types:
        todays_new_notices = notice_type.formals.filter(Q(announce_time__gte=datetime.date.today()))

        res_data = {}
        res_data['title'] = {}
        res_data['title']['icon'] = icon
        res_data['title']['title'] = title
        res_data['title']['count'] = len(todays_new_notices)
        res_data['items'] = items = []
        for idx, notice in enumerate(todays_new_notices):
            items.append({'title':notice.title, 'isnew':True, 'date':notice.announce_time, 'href':notice.paper_path})

        return res_data
    else:
        return None



