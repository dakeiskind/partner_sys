__author__ = 'chenqi'

from django.http import Http404, HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from partner.models import *
import re, json
from flows.potential.flows import PotentialApprovalFlow
from partner_sys import settings, utils

@require_POST
def sign_up(request):

    if False:
        c = Contact()
        c.name = 'contact_01'
        c.title = 'no title'
        c.tel = '110'
        c.mobile = '13800138000'
        c.idCard = 'mei you'
        c.email = '1@1.com'
        c.idCopy = 'ye mei you'
        c.save()

        p = Potential()
        p.username = 'potential_01'
        p.password = '123qwe!@#'
        p.email = '1@1.com'
        p.zh_name = u'供应商_01'
        p.en_name = 'partner_01'
        p.ceo = 'Whoever'
        p.scope = 'what?'
        p.founding = datetime.datetime.today()
        p.capital = 100000000000
        p.licence = '0101010101010'
        p.licenceCopy = 'mei you'
        p.tax = 'mei you'
        p.taxCopy = 'ye mei you'
        p.orgCode = '250'
        p.orgCodeCopy = 'mei you'
        p.employees = 3
        p.address = r'beijing'
        p.homepage = 'www.bjhjyd.gov.cn'
        p.tel = '62620202'
        p.fax = '66668888'
        p.post = u'北京市630信箱'
        p.summary = 'blahblahblah....'
        p.contact = c
        p.save()

        return JsonResponse({'contact':c.id, 'potential':p.id})

    # username = request.POST['username'].strip()
    # password = request.POST['password'].strip()
    # password_confirmed = request.POST['password_confirmed'].strip()
    # email = request.POST['email'].strip()

    signup = utils.load_json(request)
    username = signup['username'].strip()
    password = signup['password'].strip()
    password_confirmed = signup['password_confirmed'].strip()
    email = signup['email'].strip()

    username_regex = re.compile(r'[\dA-Za-z]+[\dA-Za-z_]*')
    email_regex = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b", re.IGNORECASE)

    #validate form data
    if username is None:
        return JsonResponse({'error':u'用户名不可为空'})
    if len(username) < 6:
        return JsonResponse({'error':u'用户名长度不可少于6位'})
    user_reg_m = username_regex.match(username)
    if user_reg_m is None or user_reg_m.group() != username:
        return JsonResponse({'error':u'用户名只能包含字母、数字及下划线，且必须字母或数字开头'})
    if User.objects.get(username=username) is not None:
        return JsonResponse({'error':u'此用户名已被注册'})
    if password is None or password_confirmed is None:
        return JsonResponse({'error':u'密码不可为空'})
    if password_confirmed != password:
        return JsonResponse({'error':u'密码不一致'})
    if len(password) < 8:
        return JsonResponse({'error':u'密码长度不可少于8位'})
    if email is None:
        return JsonResponse({'error':u'邮箱地址不可为空'})
    email_reg_m = email_regex.match(email)
    if email_reg_m is None or email_reg_m.group() != email:
        return JsonResponse({'error':u'邮箱地址格式不正确'})
    if User.objects.get(email=email) is not None:
        return JsonResponse({'error':u'此邮箱已被注册'})

    new_user = User.objects.create_user(username, email, password)
    new_user.save()


    #launch potential partner approval process
    # PotentialApprovalFlow.start.run()

    return JsonResponse({'info':'success'})


@require_POST
def sign_in(request):
    signin = utils.load_json(request)
    username = signin['username'].strip()
    password = signin['password'].strip()

    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({'error':u'用户名或密码错误'})
    elif user.is_active:
        login(request, user)
    else:
        return JsonResponse({'error':u'该用户已被冻结'})

    # return HttpResponseRedirect('')
    return JsonResponse({'info':'success'})


def sign_out(request):
    logout(request)

    return JsonResponse({'info':'success'})


@require_POST
@login_required()
def reset_pwd(request):
    if not request.user.is_authenticated():
        return JsonResponse({'error':u'用户没有登录'})

    reset = utils.load_json(request)
    old_pass = reset['old_pass'].strip()
    new_pass = reset['new_pass'].strip()
    new_pass_cfm = reset['new_pass_cfm'].strip()

    if old_pass is None or new_pass is None or new_pass_cfm is None:
        return JsonResponse({'error':u'密码不可为空'})

    if new_pass != new_pass_cfm:
        return JsonResponse({'error':u'新密码不一致'})
    if len(new_pass) < 8:
        return JsonResponse({'error':u'新密码长度不可少于8位'})

    # if 1 == User.objects.filter(username=request.user.username).update(password=new_pass):
    #     return JsonResponse({'info':'success'})

    user = User.objects.get(username=request.user.username)
    user.set_password(new_pass)
    user.save()

    return JsonResponse({'info':'success'})