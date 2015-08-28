__author__ = 'wangwei'

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_GET
from partner_sys import utils
from workflow.potential.models import PotentialApprovalTask

from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.http import HttpResponse
import json
from partner.models import Potential
from partner.forms import PotentialSearchForm


'''
潜在合作伙伴列表
'''
def list_potentials(request):
    response_data = _list(request, False)

    return HttpResponse(json.dumps(response_data), content_type='application/json')
    # return render_to_response('list.tpl', {'potentials' : potentials})


'''
正式合作伙伴列表
'''
def list_formals(request):
    response_data = _list(request, True)
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def search(request):
    return render_to_response('search.tpl', context_instance=RequestContext(request))

'''
潜在合作伙伴查询
'''
def query_potentials(request):
    response_data = _query(request, False)
    return HttpResponse(json.dumps(response_data), content_type='application/json')
    # return render_to_response('search.tpl', {'potentials' : potentials, 'form_data' : pd}, context_instance=RequestContext(request))


'''
潜在正式伙伴查询
'''
def query_formals(request):
    response_data = _query(request, True)
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def get_potential(request, pid):
    try:
        potential = Potential.objects.get(id=pid)
    except Potential.DoesNotExist:
        print('Record Do Not Exists!!!')

    return HttpResponse(json.dumps(potential.tojson()), content_type='application/json')
    # return render_to_response('detail.tpl', {'potential' : potential})


def _list(request, is_formal):
    potential_list = Potential.objects.filter(is_active=True, is_formal=is_formal)
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

    return response_data


def _query(request, is_formal):
    if request.method == 'POST':
        pd = utils.load_json(request)

        form = PotentialSearchForm(request.POST)
        # if form.is_valid():
        #     pd = form.cleaned_data
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

        kwargs['is_active'] = True
        kwargs['is_formal'] = is_formal

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

        return response_data