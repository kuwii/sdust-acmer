from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from database.query.group import check_user_in_group as database_check_user_in_group
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
    members = database_get_group_user(group_name)
    applicants = database_get_group_user(group_name, formal=False)

    if has_login(request) and database_check_user_in_group(group_name, request.user.username):
        in_group = True
    else:
        in_group = False

    return render(request, 'html/group_info.html', {
        'user_status': user_status(request),
        'group_info': info,
        'members': members,
        'applicants': applicants,
        'in_group': in_group
    })
