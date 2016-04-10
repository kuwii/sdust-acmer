from database.function.group import create_group as database_create_group
from database.function.group import modify_group as database_modify_group
from database.function.group import delete_group as database_delete_group
from database.function.group import join_group as database_join_group

from database.query.group import check_user_is_applicant as database_check_user_is_applicant
from database.query.group import check_user_in_group as database_check_user_in_group
from database.query.group import check_user_can_manage as database_check_user_can_manage
from database.query.group import check_user_is_boss as database_check_user_is_boss
from database.query.group import get_group as database_get_group
from database.query.group import get_group_user as database_get_group_user
from database.query.group import search_group as database_search_group

from .util import SuccessInfo, ErrorInfo

from .util import check_request
from .util import http_to_json, http_str
from .util import has_no_permission_to_do


# 查询 ------------------------------------------------------------------------------------------------------------------

def get_group(request, group_name):
    return http_to_json(database_get_group(group_name))


def get_group_user(request, group_name):
    return http_to_json(database_get_group_user(group_name))


def search_group(request, search_name):
    return http_to_json(database_search_group(query_or=True, group_name=search_name, caption=search_name))


# 修改 ------------------------------------------------------------------------------------------------------------------

def create_group_post(request):
    check = check_request(request, need_login=True, is_post=True)
    if not check.ok:
        return http_str(check.info)

    post_info = {}

    for i, j in request.POST.items():
        post_info[i] = j
        print(post_info[i])

    user = request.user
    if has_no_permission_to_do(user.username, 'manager', 'CREATE_GROUP'):
        return http_str(ErrorInfo.Permission.no_permission)

    if 'name' not in post_info:
        return http_str(ErrorInfo.Group.name_needed)
    if 'caption' not in post_info or post_info['caption'] == '':
        return http_str(ErrorInfo.Group.caption_needed)

    if 'public' in post_info:
        post_info['public'] = True if post_info['public'] == 'true' else False

    operation_result = database_create_group(user.username, **post_info)

    if not operation_result.ok:
        return http_str(ErrorInfo.Group.group_exists)

    return http_str(SuccessInfo.success)


def modify_group_post(request):
    check = check_request(request, need_login=True, is_post=True)
    if not check.ok:
        return http_str(check.info)

    post_info = {}

    for i, j in request.POST.items():
        post_info[i] = j
        print(post_info[i])

    if 'name' not in post_info:
        return http_str(ErrorInfo.Group.name_needed)

    group_name = post_info['name']

    if not database_check_user_can_manage(group_name, request.user.username):
        return http_str(ErrorInfo.Permission.no_permission)

    if 'public' in post_info:
        post_info['public'] = True if post_info['public'] == 'true' else False

    operation_result = database_modify_group(group_name, **post_info)

    if not operation_result.ok:
        return http_str(ErrorInfo.Group.group_not_exists)

    return http_str(SuccessInfo.success)


def delete_group_post(request):
    check = check_request(request, need_login=True, is_post=True)
    if not check.ok:
        return http_str(check.info)

    post_info = {}

    for i, j in request.POST.items():
        post_info[i] = j
        print(post_info[i])

    if 'name' not in post_info:
        return http_str(ErrorInfo.Group.name_needed)

    group_name = post_info['name']

    if not database_check_user_is_boss(group_name, request.user.username):
        return http_str(ErrorInfo.Permission.no_permission)

    operation_result = database_delete_group(group_name)

    if not operation_result.ok:
        return http_str(ErrorInfo.Group.group_not_exists)

    return http_str(SuccessInfo.success)


def join_group_post(request):
    check = check_request(request, need_login=True, is_post=True)
    if not check.ok:
        return http_str(check.info)

    post_info = request.POST

    if 'name' not in post_info:
        return http_str(ErrorInfo.Group.name_needed)
    group_name = post_info['name']

    group = database_get_group(group_name)
    if group is None:
        return http_str(ErrorInfo.Group.group_not_exists)

    if database_check_user_in_group(group_name, request.user.username):
        return http_str(ErrorInfo.Group.already_in_group)

    if database_check_user_is_applicant(group_name, request.user.username):
        return http_str(ErrorInfo.Group.applicant)

    database_join_group(group_name, 1 if group['public'] is True else 0, request.user.username)

    return http_str(SuccessInfo.success)
