from database.models import User, UserProfile
from database.models import UserIdentity
from database.models import UserFollowingRelation

from .util import InfoType, InfoField
from .util import operation_succeeded, operation_failed

import time


def create_user(username, password, identity_word='normal'):
    """
    创建用户。
    :param username: 用户名
    :param password: 密码
    :param identity_word: 身份
    :return: 操作结果
    """
    if User.objects.filter(username=username).exists():
        return operation_failed(InfoType.Exists, InfoField.User)
    if identity_word not in UserIdentity.IDENTITY_VALUE:
        return operation_failed(InfoType.NotExists, InfoField.IdentityWord)

    for letter in username:
        if not (letter.isalpha() or letter.isdigit() or letter == '_'):
            return operation_failed(InfoType.Invalid, InfoField.Username)

    user = User(username=username)
    user.set_password(password)
    user.save()

    profile = UserProfile(user=user)
    profile.username = username
    profile.register_time = int(time.time())
    profile.save()

    identity = UserIdentity(user=user)
    identity.level = UserIdentity.IDENTITY_VALUE[identity_word]
    identity.save()

    return operation_succeeded()


def change_password(username, new_password):
    """
    修改用户密码。
    :param username: 用户名
    :param new_password: 新密码
    :return: 操作结果
    """
    user = User.objects.filter(username=username).first()
    if user is None:
        return operation_failed(InfoType.NotExists, InfoField.User)
    user.set_password(new_password)
    user.save()

    return operation_succeeded()


def modify_info(username, new_info):
    """
    修改用户个人信息。
    :param username: 用户名
    :param new_info: 包含新用户信息的字典
    :return: 操作结果
    """
    profile = UserProfile.objects.filter(username=username).first()
    if profile is None:
        return operation_failed(InfoType.NotExists, InfoField.User)

    if 'sex' in new_info:
        sex = new_info['sex']
        if sex in UserProfile.SEX_CHOICES:
            profile.sex = sex
        else:
            return operation_failed(InfoType.Value, InfoField.UserSex)

    if 'nickname' in new_info:
        nickname = new_info['nickname']
        if nickname == '':
            nickname = None
        profile.nickname = nickname
    if 'school' in new_info:
        school = new_info['school']
        if school == '':
            school = None
        profile.school = school

    profile.save()

    return operation_succeeded()


def remove_user(username):
    """
    删除用户。
    :param username: 用户名
    :return: 操作结果
    """
    user = User.objects.filter(username=username).first()
    if user is None:
        return operation_failed(InfoType.NotExists, InfoField.User)
    user.delete()
    return operation_succeeded()


def follow_user(follower_username, following_username):
    """
    关注用户。
    :param follower_username: 关注者
    :param following_username: 被关注者
    :return: 操作结果
    """
    user1 = UserProfile.objects.filter(username=follower_username).first()
    if user1 is None:
        return operation_failed(InfoType.NotExists, InfoField.User)
    user2 = UserProfile.objects.filter(username=following_username).first()
    if user2 is None:
        return operation_failed(InfoType.NotExists, InfoField.User)

    rel = UserFollowingRelation(follower=user1, following=user2)
    rel.save()

    return operation_succeeded()


def unfollow_user(follower_username, following_username):
    """
    取消关注用户。
    :param follower_username: 关注着
    :param following_username: 被关注者
    :return: 操作结果
    """
    user1 = UserProfile.objects.filter(username=follower_username).first()
    if user1 is None:
        return operation_failed(InfoType.NotExists, InfoField.User)
    user2 = UserProfile.objects.filter(username=following_username).first()
    if user2 is None:
        return operation_failed(InfoType.NotExists, InfoField.User)

    rel = UserFollowingRelation.objects.filter(follower=user1, following=user2)
    if rel is None:
        return operation_failed(InfoType.NotExists, InfoField.UserFollowingRelation)

    rel.delete()

    return operation_succeeded()


def change_identity(username, identity_word):
    """
    修改用户权限等级
    :param username: 用户名
    :param identity_word: 权限等级，字符串
    :return:
    """
    if identity_word not in UserIdentity.IDENTITY_VALUE:
        return operation_failed(InfoType.Wrong, InfoField.IdentityWord)

    identity = UserIdentity.objects.filter(user_id=username).first()
    if identity is None:
        return operation_failed(InfoType.NotExists, InfoField.User)

    identity.level = UserIdentity.IDENTITY_VALUE[identity_word]
    identity.save()

    return operation_succeeded()
