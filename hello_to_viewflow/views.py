from django.shortcuts import render_to_response
from django.http import HttpRequest, HttpResponse
from django.template.loader import get_template
from django.template import Context
from common import models as common_models


# Create your views here.
def index(request, home):
    # Fetch common announcements
    common_annos = common_models.Announcement.formals.all()[0:9]

    # Fetch particular announcements

    # t = get_template('home.html')
    # print(t.render())
    # html = t.render(Context({'common_annos':common_annos}))

    # return render_to_response(home, {'common_annos':common_annos})
    return render_to_response(home)