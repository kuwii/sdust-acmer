from django.shortcuts import render

from database.query.problems import get_user_problems as database_get_user_problems


def problem_ajax_page(request, username, start, end):
    ret = database_get_user_problems(username, start=int(start), end=int(end))
    return render(request, 'html/problems_ajax.html', {
        'problems': ret
    })


def problem_all_ajax_page(request, username):
    ret = database_get_user_problems(username, get_all=True)
    return render(request, 'html/problems_ajax.html', {
        'problems': ret
    })
