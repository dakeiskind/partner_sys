__author__ = 'chenqi'

from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, Http404, JsonResponse
from django.template.loader import get_template
from django.template import Context
from common.models import Announcement
import json
from django.views.decorators.http import *


#common announcements list
@require_GET
def anno_list(request, page, size):
    try:
        page = int(page)
        size = int(size)
    except ValueError:
        raise Http404

    start = (page - 1) * size
    offset = start + size
    common_annos = Announcement.formals.all()[start:offset]

    response_data = {}
    response_data['title'] = ""
    response_data['link'] = ""
    response_data['href'] = ""
    response_data['datas'] = datas = []
    for idx,item in enumerate(common_annos):
        datas.append({'title':item.title, 'href':item.paper_path})

    # return HttpResponse(json.dumps(response_data), content_type="application/json")
    return JsonResponse(response_data)