from database.function.oj import create_oj as database_create_oj
from database.function.oj import modify_oj as database_modify_oj
from database.function.oj import delete_oj as database_delete_oj

from database.function.util import InfoType as database_InfoType

from .util import http_str
from .util import check_request
from .util import has_no_permission_to_do

from .util import SuccessInfo, ErrorInfo


# 修改 ------------------------------------------------------------------------------------------------------------------

def create_oj_post(request):
    check = check_request(request, need_login=True, is_post=True)
    if not check.ok:
        return http_str(check.info)

    if has_no_permission_to_do(request.user.username, 'admin', 'CREATE_OJ'):
        return http_str(ErrorInfo.Permission.no_permission)

    post_info = request.POST

    if 'name' not in post_info:
        return http_str(ErrorInfo.OJ.name_needed)
    if 'caption' not in post_info:
        return http_str(ErrorInfo.OJ.caption_needed)

    oj_info = {}
    for i, j in post_info.items():
        oj_info[i] = j if j != '' else None

    if 'available' in oj_info:
        oj_info['available'] = True if oj_info['available'] == 'true' else False

    operation_result = database_create_oj(**oj_info)

    if not operation_result.ok:
        if operation_result.info.info_type == database_InfoType.Needed:
            return http_str(ErrorInfo.OJ.name_needed)
        else:
            return http_str(ErrorInfo.OJ.oj_exists)

    return http_str(SuccessInfo.success)


def modify_oj_post(request):
    check = check_request(request, need_login=True, is_post=True)
    if not check.ok:
        return http_str(check.info)

    if has_no_permission_to_do(request.user.username, 'admin', 'MODIFY_OJ'):
        return http_str(ErrorInfo.Permission.no_permission)

    post_info = request.POST

    oj_info = {}
    for i, j in post_info.items():
        oj_info[i] = j if j != '' else None

    if 'available' in oj_info:
        oj_info['available'] = True if oj_info['available'] == 'true' else False

    operation_result = database_modify_oj(**oj_info)

    if not operation_result.ok:
        if operation_result.info.info_type == database_InfoType.Needed:
            return http_str(ErrorInfo.OJ.name_needed)
        elif operation_result.info.info_type == database_InfoType.NotExists:
            return http_str(ErrorInfo.OJ.oj_not_exists)
        elif operation_result.info.info_type == database_InfoType.Wrong:
            return http_str(ErrorInfo.OJ.caption_needed)
        else:
            return http_str(ErrorInfo.Common.just_something_wrong)

    return http_str(SuccessInfo.success)


def delete_oj_post(request):
    check = check_request(request, need_login=True, is_post=True)
    if not check.ok:
        return http_str(check.info)

    if has_no_permission_to_do(request.user.username, 'admin', 'DELETE_OJ'):
        return http_str(ErrorInfo.Permission.no_permission)

    post_info = request.POST

    if 'name' not in post_info:
        return http_str(ErrorInfo.OJ.name_needed)

    operation_result = database_delete_oj(post_info['name'])

    if not operation_result.ok:
        return http_str(ErrorInfo.OJ.oj_not_exists)

    return http_str(SuccessInfo.success)
