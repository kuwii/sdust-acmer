from django.http import HttpResponse

from database.query.permission import permitted_to_manage as database_permitted_to_manage

from database.query.permission import permitted_to_do as database_permitted_to_do
from database.query.permission import forbidden_to_do as database_forbidden_to_do
from database.query.permission import has_identity as database_has_identity

import json


class SuccessInfo:
    """
    返回的操作成功的信息
    """
    success = 'SUCCESS'


class ErrorInfo:
    """
    返回的操作失败的信息
    """
    class Common:
        just_something_wrong = 'JUST_SOMETHING_WRONG'
        exception_occurred = 'EXCEPTION_OCCURRED'

    class Request:
        wrong_request_method = 'WRONG_REQUEST_METHOD'

    class Network:
        network_error = 'NETWORK_ERROR'

    class OJ:
        caption_needed = 'OJ_CAPTION_NEEDED'
        name_needed = 'OJ_NAME_NEEDED'
        oj_exists = 'OJ_EXISTS'
        oj_not_exists = 'OJ_NOT_EXISTS'
        oj_updating = 'OJ_UPDATING'

    class Account:
        account_needed = 'ACCOUNT_NEEDED'
        account_exists = 'ACCOUNT_EXISTS'
        account_not_exists = 'ACCOUNT_EXISTS'

    class User:
        has_login = 'HAVE_LOGIN'
        not_login = 'NOT_LOGIN'
        user_exists = 'USER_EXISTS'
        user_not_exists = 'USER_NOT_EXISTS'
        user_following_not_exists = 'USER_FOLLOWING_RELATION_NOT_EXISTS'
        username_required = 'USERNAME_REQUIRED'
        password_required = 'PASSWORD_REQUIRED'
        old_password_required = 'OLD_PASSWORD_REQUIRED'
        new_password_required = 'NEW_PASSWORD_REQUIRED'
        username_or_password_wrong = 'USERNAME_OR_PASSWORD_WRONG'
        user_submission_updating = 'USER_SUBMISSION_UPDATING'
        invalid_username = 'INVALID_USER_NAME'
        wrong_sex_value = 'WRONG_SEX_VALUE'

    class Group:
        already_in_group = 'ALREADY_IN_GROUP'
        applicant = 'IS_ALREADY_APPLICANT'
        caption_needed = 'GROUP_CAPTION_NEEDED'
        group_exists = 'GROUP_EXISTS'
        group_not_exists = 'GROUP_NOT_EXISTS'
        name_needed = 'GROUP_NAME_NEEDED'
        user_relation_not_exists = 'GROUP_USER_RELATION_NOT_EXISTS'
        user_is_boss = 'GROUP_USER_IS_BOSS'
        cannot_kick_yourself = 'CANNOT_KICK_YOURSELF'
        cannot_kick_manager = 'CANNOT_KICK_MANAGER'

    class Permission:
        no_permission = 'NO_PERMISSION'
        identity_required = 'IDENTITY_REQUIRED'
        wrong_identity_word = 'WRONG_IDENTITY_WORD'
        cannot_promote = 'CANNOT_PROMOTE'


class CheckResult:
    ok = False
    info = ErrorInfo.Common.just_something_wrong

    def __init__(self, ok, info):
        self.ok = ok
        self.info = info


def http_to_json(ret):
    return HttpResponse(json.dumps(ret))


def http_str(words):
    return HttpResponse(words)


def is_himself(request, username):
    return request.user.username == username


def has_login(request):
    return request.user.is_authenticated()


def not_login(request):
    return not has_login(request)


def request_is_post(request):
    return request.method == 'POST'


def request_is_get(request):
    return request.method == 'GET'


def has_permission_to_do(username, identity_name, function_name):
    if database_forbidden_to_do(username, function_name):
        return False
    if not (database_has_identity(username, identity_name) or database_permitted_to_do(username, function_name)):
        return False
    return True


def has_no_permission_to_do(username, identity_name, function_name):
    return not has_permission_to_do(username, identity_name, function_name)


def check_request(request, need_login=None, is_post=None):
    """
    检测登录及http请求方式是否满足设定的条件。
    :param request: http请求
    :param need_login: 是否需要登录。True表示必须登录；False表示不能登录；None表示无需检测。
    :param is_post: 是否需要为post请求。True表示必须是；False表示不可是；None表示无需检测。
    :return:
    """
    if need_login is not None:
        if not_login(request):
            if need_login:
                return CheckResult(False, ErrorInfo.User.not_login)
        else:
            if need_login is False:
                return CheckResult(False, ErrorInfo.User.has_login)
    if is_post is not None:
        if request_is_post(request) != is_post:
            return CheckResult(False, ErrorInfo.Request.wrong_request_method)
    return CheckResult(True, SuccessInfo.success)


def check_can_manage(request, target_user, function_name=''):
    """
    检测当前用户能否对指定用户进行对应操作。要求必须登录且检测的两个用户不是同一个用户。
    :param request: http请求
    :param target_user: 被管理者
    :param function_name: 动作名称
    :return:
    """
    can_manage = database_permitted_to_manage(request.user.username, target_user, function_name)
    if can_manage is None:
        return CheckResult(False, ErrorInfo.User.user_not_exists)
    if not can_manage:
        return CheckResult(False, ErrorInfo.Permission.no_permission)
    return CheckResult(True, SuccessInfo.success)
