from database.models import UserProfile
from database.models import UserGroup
from database.models import UserFollowingRelation


from database.query.util import first_one, to_list, to_dict

from database.query.util import GlobalValues

QueryLimit = GlobalValues.query_limit


def get_user(username):
    """
    获取指定用户信息。
    :param username: 用户名
    :return: 如果用户存在，返回包含用户信息的字典，否则返回None
    """
    ret = first_one(UserProfile, user_id=username)
    return to_dict(ret)


def user_following(username):
    """
    获取用户关注的所有用户信息。
    :param username:
    :return:
    """
    ret = UserProfile.objects.filter(follower_relation__follower_id=username)
    return to_list(ret, get_all=True)


def user_followers(username):
    """
    获取关注用户的所有用户信息。
    :param username:
    :return:
    """
    ret = UserProfile.objects.filter(following_relation__following_id=username)
    return to_list(ret, get_all=True)


def user_has_followed(username1, username2):
    """
    检查用户是否已关注指定用户。
    :param username1: 关注者
    :param username2: 被关注者
    :return: 判断结果
    """
    return UserFollowingRelation.objects.filter(follower_id=username1, following_id=username2).exists()


def search_user(**kwargs):
    """
    搜索用户
    :param kwargs:
    :return:
    """
    if len(kwargs) == 0:
        return []

    ret = UserProfile.objects.all()

    query_or = True if 'query_or' in kwargs and kwargs['query_or'] is True else False

    if 'username' in kwargs:
        ret = ret.filter(username__icontains=kwargs['username'])
    if 'nickname' in kwargs:
        ret_t = UserProfile.objects.filter(nickname__icontains=kwargs['nickname'])
        if query_or is True:
            ret = (ret | ret_t).distinct()
        else:
            ret = ret & ret_t

    if 'start' in kwargs and 'end' in kwargs:
        start = kwargs['start']
        end = kwargs['end']
        start = start if start >= 0 else 0
        ret = ret[start: end]

    return list(ret.values())


def user_group(username):
    """
    获取用户所在的用户组。
    :param username: 用户名
    :param start: 查询结果切片的起点
    :param end: 查询结果切片的终点
    :return: 如果用户存在，返回用户所在的所有用户组，列表；否则返回空列表
    """
    user = get_user(username)
    if user is None:
        return []
    ret = user.group.all()
    return to_list(ret)


def user_updating(username):
    """
    查询用户是否在更新提交记录状态。
    :param username:
    :return:
    """
    user = first_one(UserProfile, username=username)
    if user is None:
        return None
    return user.updating
