import datetime
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template.loader import get_template
from django.template import Context
from django.db import transaction
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from viewflow.flow.task_view import flow_view

from common import models as common_models
from partner_sys import utils
from partner.models import Contact, Potential


def index(request, home):
    # Fetch common announcements
    common_annos = common_models.Announcement.formals.all()[0:9]

    # Fetch particular announcements

    # t = get_template('home.html')
    # print(t.render())
    # html = t.render(Context({'common_annos':common_annos}))

    # return render_to_response(home, {'common_annos':common_annos})
    return render_to_response(home)
