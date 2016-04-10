from database.query.category import get_category_children_analysis
from database.query.category import get_category_user_problem, get_category_basic_analysis
from database.query.category import get_category_children_analysis_users
from database.query.category import get_category_user_problem_users, get_category_basic_analysis_users

from database.models import User

from .util import http_str, http_to_json

import json


def get_user_info(request, username):
    """
    通过GET方式获得指定用户在指定目录下的数据。
    :param request:
    :param username:
    :return:
    """
    if not User.objects.filter(username=username).exists():
        return http_to_json({'categories': [], 'problems': {'solved': [], 'not_solved': [], 'not_tried': []}})
    info_get = request.GET
    if 'name' not in info_get:
        # 如果请求中不包含目录的标识，返回根结点
        return http_to_json({
            'categories': [get_category_basic_analysis('root', username)],
            'problems': {'solved': [], 'not_solved': [], 'not_tried': []}
        })
    else:
        # 如果请求中包含目录的标识，返回相应目录下的信息
        cats = get_category_children_analysis(info_get['name'], username)
        problems = get_category_user_problem(info_get['name'], username)
        return http_to_json({'categories': cats, 'problems': problems})


def get_users_info(request, user_array):
    """
    通过GET方式获得指定用户在指定目录下的数据（多个用户）
    :param request:
    :param user_array:
    :return:
    """
    users = json.loads(user_array)
    ret = []

    info_get = request.GET
    if 'name' not in info_get:
        # 如果请求中不包含目录的标识，返回根结点
        return http_to_json({
            'categories': [get_category_basic_analysis_users('root', *users)],
            'problems': [{'solved': [], 'not_solved': [], 'not_tried': []} for i in range(0, len(users))],
        })
    else:
        # 如果请求中包含目录的标识，返回相应目录下的信息
        cats = get_category_children_analysis_users(info_get['name'], *users)
        problems = get_category_user_problem_users(info_get['name'], *users)
        return http_to_json({'categories': cats, 'problems': problems})
