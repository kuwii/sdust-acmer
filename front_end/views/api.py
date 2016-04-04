from django.shortcuts import render, redirect

from .util import user_status


def api_index(request):
    return render(request, 'html/API/index.html', {
        'user_status': user_status(request)
    })
