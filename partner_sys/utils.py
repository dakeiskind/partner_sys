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
        raise ValueError(r'反序列化对象不可为空')


def to_json(object, default=None):
    if object is None:
        raise ValueError(r'反序列化对象不可为空')

    try:
        return json.dump(object, default)
    except Exception as error:
        raise RuntimeError(r'反序列化对象失败') from error