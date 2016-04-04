from database.models import User, Problem

from .util import first_one, to_list


def get_user_problems(username, **kwargs):
    """
    查询用户做过的题目
    :param username:
    :param kwargs:
    :return:
    """
    user = first_one(User, username=username)
    if user is None:
        return {'length': 0, 'slice': []}

    if 'get_all' in kwargs and kwargs['get_all']:
        data = {
            'get_all': True
        }
    else:
        data = {}
        if 'start' in kwargs:
            data['start'] = kwargs['start']
        if 'end' in kwargs:
            data['end'] = kwargs['end']

    ret = Problem.objects.filter(user=user)

    if 'tried' in kwargs and kwargs['tried'] is True:
        ret = ret.filter(user_relation__solved=True)

    ret = ret.order_by('-user_relation__first_time')

    return to_list(ret, values=[
        'pid', 'oj_caption', 'title', 'user_relation__solved', 'user_relation__first_time', 'user_relation__ac_time'
    ], **data)
