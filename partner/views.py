__author__ = 'wangwei'

from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.http import HttpResponse
from django.core import serializers
from django.http import HttpResponse
import json
from partner.models import Potential
from partner.forms import PotentialSearchForm


def list_potentials(request):
    potential_list = Potential.objects.all()
    paginator = Paginator(potential_list, 6) # 6 records / per page

    page = request.GET.get('page') # pageNo

    try:
        potentials = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        potentials = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        potentials = paginator.page(paginator.num_pages)

    list = []
    for potential in potentials:
        list.append(potential.tojson())

    response_data = {}
    response_data['potentials'] = list
    response_data['paginator.num_pages'] = potentials.paginator.num_pages
    response_data['number'] = potentials.number

    return HttpResponse(json.dumps(response_data), content_type='application/json')
    # return render_to_response('list.tpl', {'potentials' : potentials})


def search(request):
    return render_to_response('search.tpl', context_instance=RequestContext(request))


def query_potentials(request):
    if request.method == 'POST':
        form = PotentialSearchForm(request.POST)
        if form.is_valid():
            pd = form.cleaned_data
            # query
            kwargs = {}
            if pd['zh_name'] is not None and '' != pd['zh_name']:
                kwargs['zh_name__icontains'] = pd['zh_name']

            if pd['en_name'] is not None and '' != pd['en_name']:
                kwargs['en_name__icontains'] = pd['en_name']

            if pd['licence'] is not None and '' != pd['licence']:
                kwargs['licence__icontains'] = pd['licence']

            if pd['contact'] is not None and '' != pd['contact']:
                kwargs['contact__icontains'] = pd['contact']

            if pd['tax'] is not None and '' != pd['tax']:
                kwargs['tax__icontains'] = pd['tax']

            if pd['orgCode'] is not None and '' != pd['orgCode']:
                kwargs['orgCode__icontains'] = pd['orgCode']

            # pagination
            potential_list = Potential.objects.filter(**kwargs)
            paginator = Paginator(potential_list, 6) # 6 records / per page

            page = request.GET.get('page') # pageNo

            try:
                potentials = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                potentials = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                potentials = paginator.page(paginator.num_pages)

            list = []
            for potential in potentials:
                list.append(potential.tojson())

            response_data = {}
            response_data['potentials'] = list
            response_data['paginator.num_pages'] = potentials.paginator.num_pages
            response_data['number'] = potentials.number

    return HttpResponse(json.dumps(response_data), content_type='application/json')
    # return render_to_response('search.tpl', {'potentials' : potentials, 'form_data' : pd}, context_instance=RequestContext(request))


def get_potential(request, pid):
    try:
        potential = Potential.objects.get(id=pid)
    except Potential.DoesNotExist:
        print('Record Do Not Exists!!!')

    return HttpResponse(json.dumps(potential.tojson()), content_type='application/json')
    # return render_to_response('detail.tpl', {'potential' : potential})
