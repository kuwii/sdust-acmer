from ..models import ProblemCategory as __Category
from ..models import User as __User
from ..models import ProblemUserRelation as __ProblemUserRelation

from .util import first_one as __database_get
from .util import to_dict as __to_dict
from .util import to_list as __to_list


def get_category_basic(cat_name):
    """
    获取指定目录的基本信息。
    :param cat_name:
    :return: 如果目录存在，返回包含目录信息的字典，否则返回None
    """
    ret = __database_get(__Category, name=cat_name)
    return __to_dict(ret)


def get_category_children(cat_name):
    """
    获取指定目录下的所有子目录基本信息。
    :param cat_name:
    :return:
    """
    cat = __Category.objects.filter(name=cat_name).first()
    if cat is None:
        return {'length': 0, 'slice': []}
    ret = cat.category.all()
    return __to_list(ret, get_all=True)


def get_category_problem(cat_name):
    """
    获取指定目录下直接相关的问题。
    :param cat_name:
    :return:
    """
    cat = __Category.objects.filter(name=cat_name).first()
    if cat is None:
        return {'length': 0, 'slice': []}
    problems = cat.problem.filter(category_relation__direct=True)

    return __to_list(problems, get_all=True)


def get_category_basic_analysis(cat_name, username):
    """
    获取指定目录的基本信息,，并按照用户进行统计
    :param cat_name:
    :param username:
    :return: 如果目录存在，返回包含目录信息的字典，否则返回None
    """
    cat = __Category.objects.filter(name=cat_name).first()
    user = __User.objects.filter(username=username).first()
    if user is None or cat is None:
        return None

    query_dict = {}

    relation = __ProblemUserRelation.objects.filter(user=user).values('problem_id', 'solved').distinct()
    for i in relation:
        query_dict[i['problem_id']] = i['solved']

    problems = cat.problem.values('id').distinct()

    num_solved = 0
    num_tried = 0
    num_all = 0

    for problem in problems:
        if problem['id'] in query_dict:
            if query_dict[problem['id']] is True:
                num_solved += 1
            num_tried += 1
        num_all += 1

    return {
        'name': cat.name,
        'caption': cat.caption,
        'num_solved': num_solved,
        'num_tried': num_tried,
        'num_all': num_all
    }


def get_category_basic_analysis_users(cat_name, *args):
    cat = __Category.objects.filter(name=cat_name).first()
    if cat is None:
        return None

    problems = cat.problem.values('id').distinct()

    ret = []

    for username in args:
        user = __User.objects.filter(username=username).first()
        if user is None or cat is None:
            ret.append({
                'num_solved': 0,
                'num_tried': 0,
                'num_all': 0
            })
        query_dict = {}
        relation = __ProblemUserRelation.objects.filter(user=user).values('problem_id', 'solved').distinct()
        for i in relation:
            query_dict[i['problem_id']] = i['solved']

        num_solved = 0
        num_tried = 0
        num_all = 0

        for problem in problems:
            if problem['id'] in query_dict:
                if query_dict[problem['id']] is True:
                    num_solved += 1
                num_tried += 1
            num_all += 1

        ret.append({
            'num_solved': num_solved,
            'num_tried': num_tried,
            'num_all': num_all
        })

    return {
        'name': cat.name,
        'caption': cat.caption,
        'user_result': ret
    }


def get_category_children_analysis(cat_name, username):
    """
    获取指定目录下的所有子目录基本信息，并按照用户进行统计。
    :param cat_name:
    :param username :
    :return:
    """
    cat = __Category.objects.filter(name=cat_name).first()
    user = __User.objects.filter(username=username).first()
    if user is None or cat is None:
        return []

    query_dict = {}

    relation = __ProblemUserRelation.objects.filter(user=user).values('problem_id', 'solved').distinct()
    for i in relation:
        query_dict[i['problem_id']] = i['solved']

    cats = cat.category.all()
    ret = []

    for category in cats:
        problems = category.problem.values('id').distinct()

        num_solved = 0
        num_tried = 0
        num_all = 0

        for problem in problems:
            if problem['id'] in query_dict:
                if query_dict[problem['id']] is True:
                    num_solved += 1
                num_tried += 1
            num_all += 1

        ret.append({
            'name': category.name,
            'caption': category.caption,
            'num_solved': num_solved,
            'num_tried': num_tried,
            'num_all': num_all
        })

    return ret


def get_category_children_analysis_users(cat_name, *args):
    cat = __Category.objects.filter(name=cat_name).first()
    if cat is None:
        return None

    cats = cat.category.all()

    ret = []

    for category in cats:
        problems = category.problem.values('id').distinct()
        user_ret = []

        for username in args:
            user = __User.objects.filter(username=username).first()
            if user is None:
                user_ret.append({
                    'num_solved': 0,
                    'num_tried': 0,
                    'num_all': 0
                })

            query_dict = {}

            relation = __ProblemUserRelation.objects.filter(user=user).values('problem_id', 'solved').distinct()
            for i in relation:
                query_dict[i['problem_id']] = i['solved']

            num_solved = 0
            num_tried = 0
            num_all = 0

            for problem in problems:
                if problem['id'] in query_dict:
                    if query_dict[problem['id']] is True:
                        num_solved += 1
                    num_tried += 1
                num_all += 1

            user_ret.append({
                'num_solved': num_solved,
                'num_tried': num_tried,
                'num_all': num_all
            })

        ret.append({
            'name': category.name,
            'caption': category.caption,
            'user_result': user_ret
        })

    return ret


def get_category_user_problem(cat_name, username):
    """
    获取直接在指定目录下的用户AC的题目、尚未AC的题目和尚未做过的题目的情况
    :param cat_name:
    :param username:
    :return:
    """
    cat = __Category.objects.filter(name=cat_name).first()
    user = __User.objects.filter(username=username).first()
    if user is None or cat is None:
        return {'solved': [], 'not_solved': [], 'not_tried': []}

    query_dict = {}

    relation = __ProblemUserRelation.objects.filter(user=user).values('problem_id', 'solved').distinct()
    for i in relation:
        query_dict[i['problem_id']] = i['solved']

    problems = cat.problem.filter(category_relation__direct=True).values('id', 'title')

    solved = []
    not_solved = []
    not_tried = []

    for i in problems:
        if i['id'] in query_dict:
            if query_dict[i['id']] is True:
                solved.append(i)
            else:
                not_solved.append(i)
        else:
            not_tried.append(i)

    return {'solved': solved, 'not_solved': not_solved, 'not_tried': not_tried}


def get_category_user_problem_users(cat_name, *args):
    cat = __Category.objects.filter(name=cat_name).first()
    if cat is None:
        return None

    ret = []

    problems = cat.problem.filter(category_relation__direct=True).values('id', 'title')

    for username in args:
        user = __User.objects.filter(username=username).first()
        if user is None or cat is None:
            ret.append({'solved': [], 'not_solved': [], 'not_tried': []})

        query_dict = {}

        relation = __ProblemUserRelation.objects.filter(user=user).values('problem_id', 'solved').distinct()
        for i in relation:
            query_dict[i['problem_id']] = i['solved']

        solved = []
        not_solved = []
        not_tried = []

        for i in problems:
            if i['id'] in query_dict:
                if query_dict[i['id']] is True:
                    solved.append(i)
                else:
                    not_solved.append(i)
            else:
                not_tried.append(i)

        ret.append({'solved': solved, 'not_solved': not_solved, 'not_tried': not_tried})

    return ret
