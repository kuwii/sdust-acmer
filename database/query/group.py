from ..models import User
from ..models import UserGroup
from ..models import UserGroupRelation
from ..models import UserProfile

from .util import first_one, to_list, to_dict


def check_user_is_applicant(group_name, username):
    return UserGroupRelation.objects.filter(user_id=username, group_id=group_name, identity__lt=1).exists()


def check_user_in_group(group_name, username):
    return UserGroupRelation.objects.filter(user_id=username, group_id=group_name, identity__gte=1).exists()


def check_user_can_manage(group_name, username):
    return UserGroupRelation.objects.filter(user_id=username, group_id=group_name, identity__gte=2).exists()


def check_user_is_boss(group_name, username):
    return UserGroupRelation.objects.filter(user_id=username, group_id=group_name, identity=3).exists()


def get_group(group_name):
    group = first_one(UserGroup, name=group_name)
    return to_dict(group)


def get_group_user(group_name, formal=None):
    group = first_one(UserGroup, name=group_name)
    if group is None:
        return None

    if formal is True:
        users = UserProfile.objects.filter(user__group=group, user__group_rel__identity__gte=1).values()
    elif formal is False:
        users = UserProfile.objects.filter(user__group=group, user__group_rel__identity__lt=1).values()
    else:
        users = UserProfile.objects.filter(user__group=group).values()

    return to_list(users, get_all=True)


def get_user_group(username, formal=None):
    user = first_one(User, username=username)
    if username is None:
        return None

    if formal is True:
        groups = UserGroup.objects.filter(user=user, user_rel__identity__gte=1).values()
    elif formal is False:
        groups = UserGroup.objects.filter(user=user, user_rel__identity__lt=1).values()
    else:
        groups = UserGroup.objects.filter(user=user).values()

    groups = groups.values()

    return to_list(groups, get_all=True)


def search_group(**kwargs):
    if len(kwargs) == 0:
        return []

    ret = UserGroup.objects.all()

    query_or = True if 'query_or' in kwargs and kwargs['query_or'] is True else False

    if 'group_name' in kwargs:
        ret = ret.filter(name__icontains=kwargs['group_name'])
    if 'caption' in kwargs:
        ret_t = UserGroup.objects.filter(caption__icontains=kwargs['caption'])
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
