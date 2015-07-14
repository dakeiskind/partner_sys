__author__ = 'chenqi'

from django.http import Http404, HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import re

@require_POST
def sign_up(request):
    username = request.POST['username'].strip()
    password = request.POST['password'].strip()
    password_confirmed = request.POST['password_confirmed'].strip()
    email = request.POST['email'].strip()

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

    return JsonResponse({'info':'success'})


@require_POST
def sign_in(request):
    username = request.POST['username'].strip()
    password = request.POST['password'].strip()

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
# @login_required()
def reset_pwd(request):
    if not request.user.is_authenticated():
        return JsonResponse({'error':u'用户没有登录'})

    old_pass = request.POST['old_pass'].strip()
    new_pass = request.POST['new_pass'].strip()
    new_pass_cfm = request.POST['new_pass_cfm'].strip()

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