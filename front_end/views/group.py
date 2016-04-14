from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from database.query.group import check_user_is_applicant as database_check_user_is_applicant
from database.query.group import check_user_in_group as database_check_user_in_group
from database.query.group import check_user_can_manage as database_check_user_can_manage
from database.query.group import check_user_is_boss as database_check_user_is_boss
from database.query.group import get_group as database_get_group
from database.query.group import get_group_user as database_get_group_user
from database.query.group import search_group as database_search_group

from .util import user_status
from .util import has_login


def search_group(request, name, start, end):
    start = int(start)
    end = int(end)

    start = start if start >= 0 else 0
    end = end if end > start else start

    search_result = database_search_group(group_name=name, caption=name, query_or=True, start=start, end=end)

    return render(request, 'html/search_group.html', {
        'search_name': name,
        'user_status': user_status(request),
        'search_result': search_result,
        'range': {
            'start': start, 'end': end,
            'last_start': start-50, 'last_end': end-50,
            'next_start': start+50, 'next_end': end+50
        }
    })


def group_info(request, group_name):
    info = database_get_group(group_name)
    members_formal = database_get_group_user(group_name, formal=True)
    members_applicant = database_get_group_user(group_name, formal=False)
    applicants = database_get_group_user(group_name, formal=False)

    if info is None:
        return render(request, 'html/404.html', {'user_status': user_status(request)})

    is_applicant = False
    in_group = False
    can_manage = False
    is_boss = False
    if has_login(request):
        if database_check_user_is_applicant(group_name, request.user.username):
            is_applicant = True
        if database_check_user_in_group(group_name, request.user.username):
            in_group = True
        if database_check_user_can_manage(group_name, request.user.username):
            can_manage = True
        if database_check_user_is_boss(group_name, request.user.username):
            is_boss = True

    return render(request, 'html/group_info.html', {
        'user_status': user_status(request),
        'group_info': info,
        'members_formal': members_formal,
        'members_applicant': members_applicant,
        'is_applicant': is_applicant,
        'in_group': in_group,
        'can_manage': can_manage,
        'is_boss': is_boss
    })


def edit_group(request, group_name):
    if not database_check_user_is_boss(group_name, request.user.username):
        return render(request, 'html/404.html', {'user_status': user_status(request)})

    group = database_get_group(group_name)

    return render(request, 'html/group/edit_group.html', {
        'user_status': user_status(request),
        'group_info': group
    })
