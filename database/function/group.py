from ..models import UserGroup
from ..models import User
from ..models import UserGroupRelation

from .util import InfoType, InfoField
from .util import operation_succeeded, operation_failed

from .util import database_get, database_exists

import time


def create_group(username, **kwargs):
    user = database_get(User, username=username)
    if user is None:
        return operation_failed(InfoType.NotExists, InfoField.Table.User)

    if 'name' in kwargs:
        name = kwargs['name']
    else:
        return operation_failed(InfoType.Needed, InfoField.Name)

    if 'caption' in kwargs or kwargs['caption'] == "":
        caption = kwargs['caption']
    else:
        return operation_failed(InfoType.Needed, InfoField.Caption)

    if database_exists(UserGroup, name=name):
        return operation_failed(InfoType.Exists, InfoField.Table.UserGroup)

    group = UserGroup(name=name, caption=caption, register_time=int(time.time()))
    relation = UserGroupRelation(user=user, group=group, identity=3)

    if 'public' in kwargs:
        group.public = kwargs['public']
    if 'notice' in kwargs:
        group.notice = kwargs['notice']
    if 'introduction' in kwargs:
        group.introduction = kwargs['introduction']

    group.save()
    relation.save()

    return operation_succeeded()


def modify_group(group_name, **kwargs):
    group = database_get(UserGroup, name=group_name)
    if group is None:
        return operation_failed(InfoType.NotExists, InfoField.Table.UserGroup)

    if 'caption' in kwargs and kwargs['caption'] != '':
        group.caption = kwargs['caption']
    if 'public' in kwargs:
        group.public = kwargs['public']
    if 'notice' in kwargs:
        group.notice = kwargs['notice']
    if 'introduction' in kwargs:
        group.introduction = kwargs['introduction']

    group.save()

    return operation_succeeded()


def delete_group(group_name):
    group = database_get(UserGroup, name=group_name)
    if group is None:
        return operation_failed(InfoType.NotExists, InfoField.Table.UserGroup)

    group.delete()

    return operation_succeeded()


def join_group(group_name, identity_value, *args):
    """
    将用户添加至组内
    :param group_name: 组名
    :param identity_value: 等级
    :param args: 包含用户名的列表
    :return:
    """
    group = database_get(UserGroup, name=group_name)
    if group is None:
        return operation_failed(InfoType.NotExists, InfoField.Table.UserGroup)

    user_relation = []

    for username in args:
        user = database_get(User, username=username)
        if user is not None and database_get(UserGroupRelation, user=user, group=group) is None:
            user_relation.append(UserGroupRelation(user=user, group=group, identity=identity_value))
            group.member_number += 1

    group.save()
    UserGroupRelation.objects.bulk_create(user_relation)

    return operation_succeeded()


def quit_group(group_name, username):
    """
    退出用户组
    :param group_name:
    :param username:
    :return:
    """
    relation = database_get(UserGroupRelation, user_id=username, group_id=group_name)
    if relation is None:
        return operation_failed(InfoType.NotExists, InfoField.Relation.UserGroupRelation)

    relation.delete()

    group = database_get(UserGroup, name=group_name)
    group.member_number -= 1
    group.save()

    return operation_succeeded()
