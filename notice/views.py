__author__ = 'chenqi'

from django.http import HttpRequest, HttpResponse, Http404, JsonResponse
from django.views.decorators.http import *
from notice.models import *
import datetime

@require_GET
def list_bidding(request):
    res_data = __list_notice(BiddingNotice, r'../imgs/icon1.png', u'招标公告')
    return JsonResponse(res_data)

@require_GET
def list_bid(request):
    res_data = __list_notice(BidNotice, r'../imgs/icon2.png', u'中标公告')
    return JsonResponse(res_data)

@require_GET
def list_prior(request):
    res_data = __list_notice(BidNotice, r'../imgs/icon3.png', u'招标预告')
    return JsonResponse(res_data)

@require_GET
def list_change(request):
    res_data = __list_notice(BidNotice, r'../imgs/icon4.png', u'变标公告')
    return JsonResponse(res_data)

def __list_notice(notice_type, icon=r'../imgs/icon1.png', title=u'公告'):
    if type(notice_type) == BiddingNotice\
        or type(notice_type) == BidNotice\
        or type(notice_type) == PriorNotice\
        or type(notice_type) == ChangeNotice:

        todays_new_notices = notice_type.formals.filter(announce_time__gte=datetime.date.today())

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



