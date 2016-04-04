from django.contrib.auth import authenticate, login as django_login, logout as django_logout

from database.query.user import get_user as database_get_user
from database.query.user import user_following as database_user_following
from database.query.user import user_followers as database_user_followers
from database.query.user import search_user as database_search_user

from database.function.user import create_user as database_create_user
from database.function.user import change_password as database_change_password
from database.function.user import modify_info as database_modify_info
from database.function.user import remove_user as database_remove_user
from database.function.user import follow_user as database_follow_user, unfollow_user as database_unfollow_user
from database.function.user import change_identity as database_change_identity

from database.query.permission import user_identity as database_user_identity
from database.query.permission import special_permission_all as database_spacial_permission_all
from database.query.permission import can_promote as database_can_promote
from database.query.permission import identity_choices as database_identity_choices

from api.views.util import http_to_json, http_str
from api.views.util import request_is_post
from api.views.util import not_login
from api.views.util import is_himself
from api.views.util import has_no_permission_to_do

from api.views.util import check_request, check_can_manage

from api.views.util import SuccessInfo, ErrorInfo
from database.function.util import InfoType as database_InfoType, InfoField as database_InfoField


# 查询 -----------------------------------------------------------------------------------------------------------------

SEX_CHOICES = ['male', 'female']


def current_user(request):
    """
    获得当前用户的用户名。
    :param request:
    :return:
    """
    if not_login(request):
        return http_to_json(None)
    return http_to_json(request.user.username)


def current_user_info(request):
    """
    获得当前用户的信息。
    :param request:
    :return:
    """
    if not_login(request):
        return http_to_json(None)
    return http_to_json(request.user.profile)


def get_user_info(request, username):
    """
    获得指定用户的信息。
    :param request:
    :param username: 用户名
    :return:
    """
    return http_to_json(database_get_user(username=username))


def get_user_identity(request, username):
    """
    获得用户的身份信息。
    :param request:
    :param username: 用户名
    :return:
    """
    return http_to_json(database_user_identity(username))


def get_user_special_permissions(request, username):
    """
    获得用户所有的特殊权限。
    :param request:
    :param username: 用户名
    :return:
    """
    return http_to_json(database_spacial_permission_all(username))


def get_user_following(request, username, start, end):
    """
    获得用户关注的所有用户信息。
    :param request:
    :param username:
    :param start:
    :param end:
    :return:
    """
    return http_to_json(database_user_following(username, start, end))


def get_user_followers(request, username, start, end):
    """
    获得关注用户的所有用户信息。
    :param request:
    :param username:
    :param start:
    :param end:
    :return:
    """
    return http_to_json(database_user_followers(username, start, end))


def search_user_username(request, username, start, end):
    """
    按照用户名搜索用户。
    :param request:
    :param username:
    :param start:
    :param end:
    :return:
    """
    return http_to_json(database_search_user(username=username, start=start, end=end))


def search_user_nickname(request, nickname, start, end):
    """
    按照昵称搜索用户。
    :param request:
    :param nickname:
    :param start:
    :param end:
    :return:
    """
    return http_to_json(database_search_user(username=nickname, start=start, end=end))


def search_user_post(request):
    """
    高级用户搜索。
    :param request:
    :return:
    """
    if request_is_post(request):
        post_info = request.POST
    else:
        return http_str(ErrorInfo.Request.wrong_request_method)

    kwargs = {}

    if 'username' in post_info:
        kwargs['username'] = post_info['username']
    if 'nickname' in post_info:
        kwargs['nickname'] = post_info['nickname']
    if 'start' in post_info:
        kwargs['start'] = post_info['start']
    if 'end' in post_info:
        kwargs['end'] = post_info['end']

    return database_search_user(**kwargs)


def show_identity_choices(request):
    """
    显示所有的用户身份选项。
    :param request:
    :return:
    """
    return http_to_json(database_identity_choices())


def show_sex_choices(request):
    """
    显示所有的用户性别选项。
    :param request:
    :return:
    """
    return SEX_CHOICES


# 动作 ------------------------------------------------------------------------------------------------------------------

def login_post(request):
    """
    用户登录。
    :param request:
    :return:
    """
    check = check_request(request, need_login=False, is_post=True)
    if not check.ok:
        return http_str(check.info)

    post_info = request.POST

    if 'username' not in post_info:
        return http_str(ErrorInfo.User.username_required)
    if 'password' not in post_info:
        return http_str(ErrorInfo.User.password_required)

    username = post_info['username'].lower()
    password = post_info['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        if has_no_permission_to_do(username, 'normal', 'LOGIN'):
            return http_str(ErrorInfo.Permission.no_permission)

        django_login(request, user)
        return http_str(SuccessInfo.success)
    else:
        return http_str(ErrorInfo.User.username_or_password_wrong)


def logout(request):
    """
    用户注销。
    :param request:
    :return:
    """
    if not_login(request):
        return http_str(ErrorInfo.User.not_login)

    django_logout(request)
    return http_str(SuccessInfo.success)


# 修改 ------------------------------------------------------------------------------------------------------------------

def create_user_post(request):
    """
    创建用户。
    :param request:
    :return:
    """
    check = check_request(request, need_login=False, is_post=True)
    if not check.ok:
        return http_str(check.info)

    post_info = request.POST

    if 'username' not in post_info:
        return http_str(ErrorInfo.User.username_required)
    if 'password' not in post_info:
        return http_str(ErrorInfo.User.password_required)

    username = post_info['username'].lower()
    password = post_info['password']

    operation_result = database_create_user(username, password, identity_word='normal')

    if not operation_result.ok:
        if operation_result.info.info_type == database_InfoType.Exists:
            return http_str(ErrorInfo.User.user_exists)
        elif operation_result.info.info_type == database_InfoType.Invalid:
            return http_str(ErrorInfo.User.invalid_username)
        else:
            return http_str(ErrorInfo.Permission.wrong_identity_word)
    return http_str(SuccessInfo.success)


def change_password_post(request):
    """
    修改密码。
    :param request:
    :return:
    """
    check = check_request(request, need_login=True, is_post=True)
    if not check.ok:
        return http_str(check.info)

    post_info = request.POST

    if 'username' not in post_info:
        return http_str(ErrorInfo.User.username_required)
    if 'new_password' not in post_info:
        return http_str(ErrorInfo.User.new_password_required)

    username = post_info['username']
    new_password = post_info['new_password']

    if is_himself(request, username):
        # 修改密码的是本人，验证本人密码并检查权限
        if 'old_password' not in post_info:
            return http_str(ErrorInfo.User.old_password_required)
        old_password = post_info['old_password']
        user = authenticate(username=username, password=old_password)
        if user is None:
            return http_str(ErrorInfo.User.username_or_password_wrong)
        if has_no_permission_to_do(username, 'normal', 'CHANGE_PASSWORD_SELF'):
            return http_str(ErrorInfo.Permission.no_permission)
    else:
        # 修改密码的不是本人，检查权限
        check_manage = check_can_manage(request, username, 'CHANGE_PASSWORD_OTHER')
        if not check_manage.ok:
            return http_str(check_manage.info)

    operation_result = database_change_password(username, new_password=new_password)

    if not operation_result.ok:
        return http_str(ErrorInfo.User.user_not_exists)
    return http_str(SuccessInfo.success)


def modify_user_info_post(request):
    """
    修改用户信息。
    :param request:
    :return:
    """
    check = check_request(request, need_login=True, is_post=True)
    if not check.ok:
        return check.info

    post_info = request.POST

    if 'username' not in post_info:
        return http_str(ErrorInfo.User.username_required)
    username = post_info['username']

    if not is_himself(request, username):
        check_manage = check_can_manage(request, username, 'MODIFY_USER_INFO_OTHER')
        if not check_manage.ok:
            return http_str(check_manage.info)
        else:
            pass
    else:
        pass

    operation_result = database_modify_info(username, post_info)

    if not operation_result.ok:
        return http_str(ErrorInfo.User.wrong_sex_value)
    return http_str(SuccessInfo.success)


def remove_user_post(request):
    """
    删除用户
    :param request:
    :return:
    """
    check = check_request(request, need_login=True, is_post=True)
    if not check.ok:
        return http_str(check.info)

    post_info = request.POST

    if 'username' not in post_info:
        return http_str(ErrorInfo.User.username_required)
    username = post_info['username']

    check = check_can_manage(request, username, 'REMOVE_USER')
    if not check.ok:
        return check.info

    operation_result = database_remove_user(username)

    if not operation_result.ok:
        return http_str(ErrorInfo.User.user_not_exists)
    return http_str(SuccessInfo.success)


def follow_user_post(request):
    """
    关注用户
    :param request:
    :return:
    """
    check = check_request(request, need_login=True, is_post=True)
    if not check.ok:
        return http_str(check.info)

    post_info = request.POST

    if 'username' not in post_info:
        return http_str(ErrorInfo.User.username_required)
    username = post_info['username']

    if has_no_permission_to_do(request.user.username, 'normal', 'FOLLOW_USER'):
        return http_str(ErrorInfo.Permission.no_permission)

    operation_result = database_follow_user(request.user.username, username)

    if not operation_result.ok:
        return http_str(ErrorInfo.User.user_not_exists)

    return http_str(SuccessInfo.success)


def unfollow_user_post(request):
    check = check_request(request, need_login=True, is_post=True)
    if not check.ok:
        return http_str(check.info)

    post_info = request.POST

    if 'username' not in post_info:
        return http_str(ErrorInfo.User.username_required)
    username = post_info['username']

    if has_no_permission_to_do(request.user.username, 'normal', 'UNFOLLOW_USER'):
        return http_str(ErrorInfo.Permission.no_permission)

    operation_result = database_unfollow_user(request.user.username, username)

    if not operation_result.ok:
        if operation_result.info.info_field == database_InfoField.User:
            return http_str(ErrorInfo.User.user_not_exists)
        else:
            return http_str(ErrorInfo.User.user_following_not_exists)

    return http_str(SuccessInfo.success)


def change_identity_post(request):
    check = check_request(request, need_login=True, is_post=True)
    if not check.ok:
        return http_str(check.info)

    post_info = request.POST

    if 'username' not in post_info:
        return http_str(ErrorInfo.User.username_required)
    if 'identity' not in post_info:
        return http_str(ErrorInfo.Permission.identity_required)
    username = post_info['username']
    identity = post_info['identity']

    check_manage = check_can_manage(request, username, 'CHANGE_IDENTITY')
    if not check_manage.ok:
        return http_str(check_manage.info)

    if identity not in database_identity_choices():
        return http_str(ErrorInfo.Permission.wrong_identity_word)

    if not database_can_promote(request.user.username, identity):
        return http_str(ErrorInfo.Permission.cannot_promote)

    operation_result = database_change_identity(username, identity)

    if not operation_result.ok:
        return http_str(ErrorInfo.User.user_not_exists)

    return http_str(SuccessInfo.success)


def add_special_permission_post(request):
    pass


def remove_special_permission_post(request):
    pass
