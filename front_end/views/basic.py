from django.shortcuts import render, redirect

from .util import user_status


def to_home(request):
    return redirect('/home', {
        'user_status': user_status(request)
    })


def homepage(request):
    return render(request, 'html/home.html', {
        'user_status': user_status(request)
    })


def faq(request):
    return render(request, 'html/FAQ.html', {
        'user_status': user_status(request)
    })
