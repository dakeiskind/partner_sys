__author__ = 'chenqi'

from django.http import Http404, HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import *
from django.contrib.auth import authenticate, login


def sign_up(reuqest):

    return


@require_POST
def sign_in(request):
    username = request.POST['username']
    passwd = request.POST['password']

    user = authenticate(username=username, password=passwd)
    if user is None:
        return JsonResponse({'error':'用户不存在'})
    elif user.is_active:
        login(request, user)
    else:
        return JsonResponse({'error':'该用户已被冻结'})

    # return HttpResponseRedirect('')
    return JsonResponse({'info':'success'})

def sign_out(request):

    return


def reset_pwd(request):

    return