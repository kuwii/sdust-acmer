from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from database.query.oj import oj_all as database_oj_all
from database.query.user import get_user as database_get_user
from database.query.user import user_has_followed as database_user_has_followed
from database.query.user import search_user as database_search_user
from database.query.user import user_following as database_user_following
from database.query.user import user_followers as database_user_followers
from database.query.permission import permitted_to_manage as database_permitted_to_manage
from database.query.accounts import get_accounts as database_get_accounts

from .util import user_status, has_login


def sign_in(request):
    if has_login(request):
        return redirect('/home/')

    return render(request, 'html/sign_in.html', {
        'user_status': user_status(request)
    })


def sign_up(request):
    if has_login(request):
        return redirect('/home/')

    return render(request, 'html/sign_up.html', {
        'user_status': user_status(request)
    })


@login_required(login_url='/user/login/')
def settings(request, username):
    is_himself = (request.user.username == username)

    if not (is_himself or database_permitted_to_manage(request.user.username, username, 'MODIFY_USER_OTHER')):
        return HttpResponse('No Permission')

    user_info = database_get_user(username)
    if user_info is None:
        return render(request, 'html/404.html', {
            'user_status': user_status(request)
        })

    accounts = database_get_accounts(username=username, get_all=True)

    return render(request, 'html/settings.html', {
        'user_status': user_status(request),
        'is_himself': is_himself,
        'user_info': user_info,
        'accounts': accounts,
        'oj_all': database_oj_all()
    })


def training_information(request, username):
    is_himself = (request.user.username == username)

    user_info = database_get_user(username)
    if user_info is None:
        return render(request, 'html/404.html', {
            'user_status': user_status(request)
        })
    if user_info['nickname'] is None:
        user_info['nickname'] = user_info['username']

    can_manage = False
    if has_login(request):
        if database_permitted_to_manage(request.user.username, username, 'MODIFY_USER_OTHER'):
            can_manage = True

    return render(request, 'html/training_information.html', {
        'user_status': user_status(request),
        'user_info': user_info,
        'is_himself': is_himself,
        'can_manage': can_manage,
        'has_followed': database_user_has_followed(request.user.username, username)
    })


def search_user(request, name, start, end):
    start = int(start)
    end = int(end)

    start = start if start >= 0 else 0
    end = end if end > start else start

    search_result = database_search_user(username=name, nickname=name, query_or=True, start=start, end=end)

    return render(request, 'html/search_user.html', {
        'search_name': name,
        'user_status': user_status(request),
        'search_result': search_result,
        'range': {
            'start': start, 'end': end,
            'last_start': start-50, 'last_end': end-50,
            'next_start': start+50, 'next_end': end+50
        }
    })


def following_followers(request, username):
    user_info = database_get_user(username)
    if user_info is None:
        return render(request, 'html/404.html', {
            'user_status': user_status(request)
        })

    if request.user.username != username:
        return render(request, 'html/404.html', {
            'user_status': user_status(request)
        })

    can_manage = False
    if has_login(request):
        if database_permitted_to_manage(request.user.username, username, 'MODIFY_USER_OTHER'):
            can_manage = True

    following = database_user_following(username)
    followers = database_user_followers(username)

    return render(request, 'html/following_followers.html', {
        'user_status': user_status(request),
        'can_manage': can_manage,
        'following': following,
        'followers': followers,
        'following_number': len(following['slice']),
        'followers_number': len(followers['slice'])
    })
