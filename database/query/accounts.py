from database.models import OJAccount

from .util import first_one, to_dict, to_list

from .util import GlobalValues


def get_account(**kwargs):
    """
    按照帐号的ID或者帐号所属的用户和OJ获取指定帐号。
    :param kwargs:
    :return: 如果ID存在，返回包含对应帐号信息的字典，否则返回None
    """
    if 'id' in kwargs:
        ret = first_one(OJAccount, id=kwargs['id'])
    elif 'username' in kwargs and 'oj_name' in kwargs:
        ret = first_one(OJAccount, user_id=kwargs['username'], OJ_id=kwargs['oj_name'])
    else:
        return None

    return to_dict(ret)


def get_accounts(**kwargs):
    """
    依照OJ和用户名搜索OJ帐号，OJ名和用户名不可同时为空。
    :param kwargs:
    :return: 搜索结果，列表
    """
    ret = OJAccount.objects

    if 'id' in kwargs:
        ret = ret.filter(id=kwargs['id'])
    if 'username' in kwargs:
        ret = ret.filter(user_id=kwargs['username'])
    if 'oj_name' in kwargs:
        ret = ret.filter(OJ_id=kwargs['oj_name'])

    if 'get_all' in kwargs and kwargs['get_all']:
        return to_list(ret, get_all=True)
    else:
        if 'start' in kwargs and 'end' in kwargs:
            start = kwargs['start']
            end = kwargs['end']
        else:
            start = 0
            end = GlobalValues.query_limit
        return to_list(ret, start=start, end=end)
