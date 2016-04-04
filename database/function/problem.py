from database.models import OJ, Problem

from .util import operation_succeeded, operation_failed
from .util import database_get

from .util import InfoType, InfoField

import time


def lock_oj_updating(oj_name):
    """
    当OJ更新时锁定OJ，避免重复更新造成冲突。
    :param oj_name: OJ的name项
    :return: 操作结果
    """
    oj = database_get(OJ, name=oj_name)
    if oj is None:
        return operation_failed(InfoType.NotExists, InfoField.OJ)
    oj.updating = True
    oj.save()

    return operation_succeeded()


def unlock_oj_updating(oj_name):
    """
    当OJ更新完成时解锁OJ。
    :param oj_name: OJ的name项
    :return: 操作结果
    """
    oj = database_get(OJ, name=oj_name)
    if oj is None:
        return operation_failed(InfoType.NotExists, InfoField.OJ)
    oj.updating = False
    oj.save()

    return operation_succeeded()


def update_problems(oj_name, problem_list, **kwargs):
    oj = database_get(OJ, name=oj_name)
    if oj is None:
        return operation_failed(InfoType.NotExists, InfoField.Table.OJ)

    incrementally = 'incrementally' in kwargs and kwargs['incrementally'] is True

    old_problems_values_id = Problem.objects.filter(oj_id=oj_name).values('index_id')
    old_problems_id = set()
    for problem in old_problems_values_id:
        old_problems_id.add(problem['index_id'])

    new_problems = []
    try:
        for problem in problem_list:
            if problem['index_id'] in old_problems_id:
                continue

            problem['oj'] = oj
            problem['oj_caption'] = oj.caption

            problem_create = Problem(**problem)
            new_problems.append(problem_create)

        Problem.objects.bulk_create(new_problems)

        oj.last_update_time = time.time()
        oj.save()
    except:
        return operation_failed(InfoType.Unknown, InfoField.Null)

    return operation_succeeded()
