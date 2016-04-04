from django.shortcuts import render

from database.query.submissions import get_user_submissions as database_get_user_submissions


def submission_ajax_page(request, username, start, end):
    ret = database_get_user_submissions(username, start=int(start), end=int(end))
    return render(request, 'html/submissions_ajax.html', {
        'submissions': ret
    })


def submission_all_ajax_page(request, username):
    ret = database_get_user_submissions(username, get_all=True)
    return render(request, 'html/submissions_ajax.html', {
        'submissions': ret
    })