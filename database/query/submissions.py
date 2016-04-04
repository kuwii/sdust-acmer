from database.models import User, Submission

from .util import first_one, to_list


def get_user_submissions(username, **kwargs):
    """
    查询用户的所有提交记录。
    :param username: 用户名
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

    ret = Submission.objects.filter(user=user).order_by('-sub_time')

    return to_list(ret, **data)
