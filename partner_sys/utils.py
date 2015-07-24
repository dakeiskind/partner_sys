__author__ = 'chenqi'

import json
from django.http import HttpRequest
from partner_sys import settings

def load_json(request):
    if not isinstance(request, HttpRequest):
        raise TypeError('bad operand type')

    try:
        json_str=((request.body).decode(settings.ENCODING))
        json_obj=json.loads(json_str)
        return json_obj
    except:
        print('Loading json string failed.')