from crawler.query import get_submissions as crawler_get_submissions

from database.function.submission import lock_user_updating as database_lock_user_updating
from database.function.submission import unlock_user_updating as database_unlock_user_updating
from database.function.submission import update_submissions as database_update_submissions

from database.query.oj import get_oj as database_get_oj
from database.query.user import get_user as database_get_user
from database.query.accounts import get_accounts as database_get_accounts

from .util import is_himself
from .util import check_request, check_can_manage
from .util import has_no_permission_to_do
from .util import http_str
from .util import SuccessInfo, ErrorInfo


def update_submission_post(request):
    check = check_request(request, need_login=True, is_post=True)
    if not check.ok:
        return http_str(check.info)

    post_info = request.POST

    if 'username' not in post_info:
        return http_str(ErrorInfo.User.username_required)
    username = post_info['username']

    user = database_get_user(username)
    if user is None:
        return http_str(ErrorInfo.User.user_not_exists)

    # 检查权限
    if is_himself(request, username):
        if has_no_permission_to_do(username, 'normal', 'UPDATE_SUBMISSION_SELF'):
            return http_str(ErrorInfo.Permission.no_permission)
    else:
        check_manage = check_can_manage(request, username, 'UPDATE_SUBMISSION_OTHER')
        if not check_manage.ok:
            return http_str(check_manage.info)

    if user['updating'] is True:
        return http_str(ErrorInfo.User.user_submission_updating)

    database_lock_user_updating(username)

    oj_updated = 0

    accounts = database_get_accounts(username=username, get_all=True)['slice']
    for account in accounts:
        oj = database_get_oj(account['OJ_id'])
        crawler_name = oj['crawler_submission']

        submissions = crawler_get_submissions(crawler_name, account['account'])
        if submissions is False:
            continue

        operation_result = database_update_submissions(username, oj['name'], submissions)
        if operation_result.ok:
            oj_updated += 1

    database_unlock_user_updating(username)

    return http_str('Successfully updated information on '+str(oj_updated)+' OJ.')
