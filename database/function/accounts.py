from database.models import User, OJ, OJAccount

from .util import InfoType, InfoField

from .util import operation_succeeded, operation_failed
from .util import database_get, database_exists


def create_account(oj_name, username, account_name):
    """
    创建用户帐号。
    :param oj_name: OJ的标识
    :param username: 用户名
    :param account_name: 帐户名
    :return: 操作结果
    """
    oj = database_get(OJ, name=oj_name)
    if oj is None:
        return operation_failed(InfoType.NotExists, InfoField.OJ)
    user = database_get(User, username=username)
    if user is None:
        return operation_failed(InfoType.NotExists, InfoField.User)

    if database_exists(OJAccount, OJ_id=oj_name, account=account_name)\
            or database_exists(OJAccount, OJ_id=oj_name, user_id=username):
        return operation_failed(InfoType.Exists, InfoField.Table.Account)

    account = OJAccount(OJ=oj, OJ_caption=oj.caption, user=user, account=account_name)
    account.save()

    return operation_succeeded()


def delete_account(oj_name, username):
    """
    删除用户在指定OJ上的帐号。
    :param oj_name: OJ的标识
    :param username: 用户名
    :return: 操作结果
    """
    account = database_get(OJAccount, OJ_id=oj_name, user_id=username)
    if account is None:
        return operation_failed(InfoType.NotExists, InfoField.Table.Account)

    account.delete()

    return operation_succeeded()


def change_account(oj_name, username, account_name):
    """
    更换用户在指定OJ上的帐号。
    :param oj_name: OJ的标识
    :param username: 用户名
    :param account: 操作结果
    :return:
    """
    old_account = database_get(OJAccount, OJ_id=oj_name, user_id=username)

    create_operation = create_account(oj_name, username, account_name)
    if not create_operation.ok:
        return operation_failed(create_operation.info.info_type, create_operation.info.info_field)

    if old_account is not None:
        old_account.delete()

    return operation_succeeded()
