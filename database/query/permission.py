from database.models import User, UserProfile, UserStudent
from database.models import UserIdentity, UserPermission, UserPermissionRelation
from database.models import UserGroup, UserGroupRelation

from database.query.util import to_list, first_one, to_dict


IDENTITY_CHOICES = UserIdentity.IDENTITY_WORD.values()


def identity_choices():
    return IDENTITY_CHOICES


def user_identity(username):
    """
    获得指定用户的权限等级。
    :param username: 待查询用户的用户名
    :return: 若用户存在，返回字典，"level"键对应权限值，"name"键对应权限代表的等级；否则返回None
    """
    identity = first_one(UserIdentity, user_id=username)
    if identity is None:
        return None

    return {
        'level': identity.level,
        'name': identity.get_level_display()
    }


def can_manage(username1, username2):
    """
    不考虑页特殊权限，判断指定用户能否管理另一指定用户。
    :param username1: 需要判断是否为管理者的用户的用户名
    :param username2: 需要判断是否为被管理者的用户的用户名
    :return: 如果两个用户均存在，返回判断结果；如果两个用户中的任意一个不存在，返回None
    """
    identity1 = first_one(UserIdentity, user_id=username1)
    identity2 = first_one(UserIdentity, user_id=username2)
    if identity1 is None or identity2 is None:
        return None
    elif identity1 == 0:
        return False
    else:
        return identity1.level < UserIdentity.IDENTITY_VALUE['normal'] and identity1.level < identity2.level


def permitted_to_manage(username1, username2, function_name):
    """
    结合用户特殊权限判断用户是否能够管理另一指定用户。
    :param username1: 需要判断是否为管理者的用户的用户名
    :param username2: 需要判断是否为被管理者的用户的用户名
    :param function_name: 执行的动作名称
    :return: 如果两个用户均存在，返回判断结果；如果两个用户中的任意一个不存在，返回None
    """
    identity1 = first_one(UserIdentity, user_id=username1)
    identity2 = first_one(UserIdentity, user_id=username2)
    if identity1 is None or identity2 is None:
        return None
    elif identity1 == 0:
        return False
    elif identity1.level < UserIdentity.IDENTITY_VALUE['normal'] and identity1.level < identity2.level:
        return True

    special_permission = UserPermissionRelation.objects.filter(
        user_id=username1, function_id=function_name, allowed=True
    )
    for permission in special_permission:
        if permission.level < UserIdentity.IDENTITY_VALUE['normal'] and permission.level < identity2.level:
            return True
    return False


def can_promote(username, identity_word):
    identity = first_one(UserIdentity, user_id=username)
    if identity is None:
        return None

    level = identity.level
    target_level = UserIdentity.IDENTITY_VALUE[identity_word]

    return level < UserIdentity.IDENTITY_VALUE['normal'] and level < target_level


def has_identity(username, identity_word):
    """
    判断指定用户是否具有具体身份的权限。
    :param username: 用户名
    :param identity_word: 权限身份，字符串，参见models.py中定义
    :return: 如果用户和权限身份均存在，返回判断结果；否则返回None
    """
    identity = first_one(UserIdentity, user_id=username)
    if identity is None:
        return None
    if identity_word not in UserIdentity.IDENTITY_VALUE:
        return None
    level = UserIdentity.IDENTITY_VALUE[identity_word]
    return identity.level != 0 and identity.level <= level


def get_identity_map(username):
    """
    获得用户身份权限的情况。
    :param username: 用户名
    :return: 字典，key为身份名称，value为是否具有该身份的权限
    """
    identity = first_one(UserIdentity, user_id=username)
    if identity is None:
        return None

    level = identity.level
    ret = {}
    for (number, word) in UserIdentity.IDENTITY_WORD.items():
        if level != 0 and identity.level <= number:
            ret[word] = True
        else:
            ret[word] = False
    if level == 0:
        ret['disabled'] = True

    return ret


def special_permission_all(username):
    """
    查询用户可以执行的所有特殊权限。
    :param username: 用户名
    :return: 列表形式返回用户可以执行的所有动作名
    """
    ret = UserPermissionRelation.objects.filter(user_id=username).values(
        'allowed', 'level', 'function__function', 'function__explanation'
    )
    return list(ret)


def permitted_to_do(username, function_name):
    """
    判断指定用户是否具有指定动作的权限。
    :param username: 用户名
    :param function_name:动作名
    :return: 如果用户存在，返回判断结果；否则返回None
    """
    if UserPermissionRelation.objects.filter(user_id=username, function_id=function_name, allowed=True).exists():
        return True
    return False


def forbidden_to_do(username, function_name):
    """
    判断指定用户是否被禁止有指定动作的权限。
    :param username: 用户名
    :param function_name: 动作名
    :return: 如果用户存在，返回判断结果；否则返回None
    """
    if UserPermissionRelation.objects.filter(user_id=username, function_id=function_name, allowed=False).exists():
        return True
    return False


def can_do(username, identity_word, function_name):
    """
    结合用户的身份权限以及特定权限判断用户是否拥有执行特定动作的权限。
    :param username: 用户名
    :param identity_word: 权限身份，字符串，参见models.py中定义
    :param function_name: 动作名
    :return: 如果用户和权限身份均存在，返回判断结果；否则返回None
    """
    if not has_identity(username, identity_word):
        return False
    if forbidden_to_do(username, function_name):
        return False
    return permitted_to_do(username, function_name)
