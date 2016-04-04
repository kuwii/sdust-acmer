from database.query.accounts import get_accounts as database_get_accounts

from database.function.accounts import create_account as database_create_account
from database.function.accounts import delete_account as database_delete_account

from .util import SuccessInfo, ErrorInfo

from .util import http_str, http_to_json
from .util import check_request, check_can_manage, is_himself, has_no_permission_to_do


# 查询 -----------------------------------------------------------------------------------------------------------------

def user_accounts_all(request, username):
    accounts = database_get_accounts(username=username, get_all=True)
    return http_to_json(accounts)


# 修改 ------------------------------------------------------------------------------------------------------------------

def create_account_post(request):
    check = check_request(request, need_login=True, is_post=True)
    if not check.ok:
        return check.info

    post_info = request.POST

    if 'username' not in post_info:
        return http_str(ErrorInfo.User.username_required)
    username = post_info['username']
    if 'oj_name' not in post_info:
        return http_str(ErrorInfo.OJ.name_needed)
    oj_name = post_info['oj_name']
    if 'account' not in post_info:
        return http_str(ErrorInfo.Account.account_needed)
    account = post_info['account']

    if not is_himself(request, username):
        check = check_can_manage(request, username, 'ADD_ACCOUNT_OTHER')
        if not check.ok:
            return http_str(check.info)
    else:
        if has_no_permission_to_do(username, 'normal', 'ADD_ACCOUNT_SELF'):
            return http_str(ErrorInfo.Permission.no_permission)

    operation_result = database_create_account(oj_name, username, account)

    if not operation_result.ok:
        return http_str(ErrorInfo.Account.account_exists)

    return http_str(SuccessInfo.success)


def delete_account_post(request):
    check = check_request(request, need_login=True, is_post=True)
    if not check.ok:
        return http_str(check.info)

    post_info = request.POST

    if 'username' not in post_info:
        return http_str(ErrorInfo.User.username_required)
    username = post_info['username']
    if 'oj_name' not in post_info:
        return http_str(ErrorInfo.OJ.name_needed)
    oj_name = post_info['oj_name']

    if not is_himself(request, username):
        check = check_can_manage(request, username, 'DELETE_ACCOUNT_OTHER')
        if not check.ok:
            return http_str(check.info)
    else:
        if has_no_permission_to_do(username, 'normal', 'DELETE_ACCOUNT_SELF'):
            return http_str(ErrorInfo.Permission.no_permission)

    operation_result = database_delete_account(oj_name, username)

    if not operation_result.ok:
        return http_str(ErrorInfo.Account.account_not_exists)

    return http_str(SuccessInfo.success)
