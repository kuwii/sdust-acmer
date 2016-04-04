from crawler.query import get_problems as __crawler_get_problems

from database.query.oj import get_oj as __database_get_oj
from database.query.oj import oj_updating as __database_oj_updating

from database.function.problem import lock_oj_updating as __database_lock_oj_updating
from database.function.problem import unlock_oj_updating as __database_unlock_oj_updating
from database.function.problem import update_problems as __database_update_problems

from database.function.util import InfoType as __database_InfoType

from .util import http_str as __http_str
from .util import check_request as __check_request
from .util import has_no_permission_to_do

from .util import SuccessInfo, ErrorInfo


def update_problems_post(request):
    check = __check_request(request, need_login=True, is_post=True)
    if not check.ok:
        return __http_str(check.info)

    if has_no_permission_to_do(request.user.username, 'admin', 'UPDATE_PROBLEMS'):
        return __http_str(ErrorInfo.Permission.no_permission)

    post_info = request.POST

    if 'oj_name' not in post_info:
        return __http_str(ErrorInfo.OJ.name_needed)
    oj_name = post_info['oj_name']

    oj = __database_get_oj(oj_name)
    if oj is None:
        return __http_str(ErrorInfo.OJ.oj_not_exists)
    if __database_oj_updating(oj_name):
        return __http_str(ErrorInfo.OJ.oj_updating)

    __database_lock_oj_updating(oj_name)

    try:
        print('Crawling problems of '+oj_name)

        problems = __crawler_get_problems(oj['crawler_problem'])
        if problems is False:
            return __http_str(ErrorInfo.Network.network_error)

        print('Updating problems of '+oj_name)

        operation_result = __database_update_problems('uva', problems)
    finally:
        __database_unlock_oj_updating(oj_name)
    
    if not operation_result.ok:
        if operation_result.info.info_type == __database_InfoType.Unknown:
            return __http_str(ErrorInfo.Common.exception_occurred)

    return __http_str(SuccessInfo.success)
