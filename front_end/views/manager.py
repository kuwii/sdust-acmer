from django.shortcuts import render
from django.http import HttpResponse

from django import forms

from django.contrib.auth.decorators import login_required

from database.function.category import create_oj_category

from database.query.oj import oj_all as database_oj_all
from database.query.oj import get_oj as database_get_oj

from .util import user_status

import xmltodict


@login_required(login_url='/user/login/')
def manager_page(request):
    u_status = user_status(request)
    if u_status['identity']['manager'] is False:
        return HttpResponse('No Permission')

    return render(request, 'html/manager/for_managers.html', {
        'user_status': u_status,
    })
