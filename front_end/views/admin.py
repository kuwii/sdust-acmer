from django.shortcuts import render
from django.http import HttpResponse

from django import forms

from django.contrib.auth.decorators import login_required

from database.function.category import create_oj_category

from database.query.oj import oj_all as database_oj_all
from database.query.oj import get_oj as database_get_oj

from .util import user_status

import xmltodict


# Util -----------------------------------------------------------------------------------------------------------------

class CategoryXMLForm(forms.Form):
    file = forms.FileField(required=True)


# Page -----------------------------------------------------------------------------------------------------------------

@login_required(login_url='/user/login/')
def admin_page(request):
    u_status = user_status(request)
    if u_status['identity']['admin'] is False:
        return HttpResponse('No Permission')

    oj = database_oj_all()

    return render(request, 'html/admin/for_site_administrators.html', {
        'user_status': u_status,
        'oj_all': oj
    })


@login_required(login_url='/user/login/')
def new_oj(request):
    u_status = user_status(request)
    if u_status['identity']['admin'] is False:
        return HttpResponse('No Permission')

    return render(request, 'html/admin/new_oj.html', {
        'user_status': u_status
    })


@login_required(login_url='/user/login/')
def edit_oj(request, oj_name):
    u_status = user_status(request)
    if u_status['identity']['admin'] is False:
        return HttpResponse('No Permission')

    oj = database_get_oj(oj_name)
    if oj is None:
        return render(request, 'html/404.html', {
            'user_status': u_status
        })

    return render(request, 'html/admin/edit_oj.html', {
        'user_status': u_status,
        'oj': oj
    })


@login_required(login_url='/user/login/')
def upload_xml(request, oj_name):
    u_status = user_status(request)
    if u_status['identity']['admin'] is False:
        return HttpResponse('No Permission')

    oj = database_get_oj(oj_name)
    if oj is None:
        return render(request, 'html/404.html', {
            'user_status': u_status
        })

    error = False
    error_info = None
    upload = False

    if request.method == 'POST':
        upload = True

        form = CategoryXMLForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.cleaned_data['file']
        else:
            return render(request, 'html/admin/oj_upload_xml.html', {
                'user_status': u_status,
                'form': form,
                'oj': oj,
                'upload': True,
                'error': True
            })

        xml_str = ''
        for chunk in file.chunks():
            xml_str += chunk.decode('utf8', 'ignore')

        cat_dict = xmltodict.parse(xml_str)

        ret = create_oj_category(oj_name, cat_dict)

        if not ret.ok:
            error = True
            error_info = ret.info
    else:
        form = CategoryXMLForm()

    return render(request, 'html/admin/oj_upload_xml.html', {
        'user_status': u_status,
        'form': form,
        'oj': oj,
        'upload': upload,
        'error': error,
        'error_info': error_info
    })
