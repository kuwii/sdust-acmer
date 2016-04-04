from database.models import OJ, OJAccount, User, UserProfile, Submission, Problem, ProblemUserRelation

from .util import operation_succeeded, operation_failed
from .util import database_get

from .util import InfoType, InfoField

from time import time as __time


def lock_user_updating(username):
    """
    当用户更新提交记录时锁定用户，避免重复更新造成冲突。
    :param username: 用户名
    :return: 操作结果
    """
    user_profile = database_get(UserProfile, username=username)
    if user_profile is None:
        return operation_failed(InfoType.NotExists, InfoField.User)
    user_profile.updating = True
    user_profile.save()

    return operation_succeeded()


def unlock_user_updating(username):
    """
    当用户更新提交记录完成时时解锁用户。
    :param username: 用户名
    :return: 操作结果
    """
    user_profile = database_get(UserProfile, username=username)
    if user_profile is None:
        return operation_failed(InfoType.NotExists, InfoField.User)
    user_profile.updating = False
    user_profile.save()

    return operation_succeeded()


def update_submissions(username, oj_name, submission_list, **kwargs):
    user = database_get(User, username=username)
    if user is None:
        return operation_failed(InfoType.NotExists, InfoField.Table.User)
    user_profile = user.profile

    account = database_get(OJAccount, OJ_id=oj_name, user=user)
    if account is None:
        return operation_failed(InfoType.NotExists, InfoField.Table.Account)

    oj = database_get(OJ, name=oj_name)
    if oj is None:
        return operation_failed(InfoType.NotExists, InfoField.Table.OJ)

    incrementally = 'incrementally' in kwargs and kwargs['incrementally'] is True

    old_problems = Problem.objects.filter(oj_id=oj_name)

    old_submissions_values_id = Submission.objects.filter(oj_id=oj_name).values('sid')
    old_submissions_id = set()
    for submission in old_submissions_values_id:
        old_submissions_id.add(submission['sid'])

    new_submission = []


    relation_dict = {}
    num_tried = 0
    num_solved = 0

    ProblemUserRelation.objects.filter(user=user).delete()

    for submission in submission_list:
        # 检查题目是否存在
        problem = old_problems.filter(index_id=submission['index_id']).first()
        if problem is None:
            continue

        # 检查用户与题目的关系
        if problem.id in relation_dict:
            # 如果关系已经建立，检查提交时间
            relation = relation_dict[problem.id]
            if submission['sub_time'] < relation.first_time:
                relation.first_time = submission['sub_time']
        else:
            # 如果关系不存在，创建关系
            relation = ProblemUserRelation(user=user, problem=problem, first_time=submission['sub_time'])
            num_tried += 1
        if submission['solved']:
            # 如果题目检测结果为通过
            if relation.solved:
                # 如果已存在通过的关系，检查通过时间
                if submission['sub_time'] < relation.ac_time:
                    relation.ac_time = submission['sub_time']
            else:
                # 如果题目之前不存在通过的提交，修改关系
                relation.solved = True
                relation.ac_time = submission['sub_time']
                num_solved += 1
        relation_dict[problem.id] = relation

        # 检查提交记录是否已经存在
        if submission['sid'] in old_submissions_id:
            continue
        # 添加外键
        submission['user'] = user
        submission['account'] = account
        submission['account_account'] = account.account
        submission['oj'] = oj
        submission['oj_caption'] = oj.caption
        submission['problem'] = problem
        submission['problem_pid'] = problem.pid
        submission['problem_title'] = problem.title
        submission['problem_time_limit'] = problem.time_limit
        submission['problem_memory_limit'] = problem.memory_limit

        submission.pop('index_id')
        submission.pop('solved')

        submission_create = Submission(**submission)
        new_submission.append(submission_create)

    # 批量写入数据库
    Submission.objects.bulk_create(new_submission)
    ProblemUserRelation.objects.bulk_create(list(relation_dict.values()))

    user_profile.last_update_time = int(__time())
    user_profile.submission_number += len(new_submission)
    user_profile.problem_tried_number = num_tried
    user_profile.problem_solved_number = num_solved

    user_profile.save()

    return operation_succeeded()
