from database.models import ProblemCategory, OJ
from database.models import ProblemCategoryCategoryRelation, ProblemCategoryProblemRelation

from .util import InfoType, InfoField
from .util import operation_succeeded, operation_failed
from .util import database_get, database_exists


def create_category(**kwargs):
    """
    创建目录
    :param kwargs:
    :return:
    """
    if 'name' not in kwargs or kwargs['name'] == '':
        return operation_failed(InfoType.Needed, InfoField.Name)
    name = kwargs['name']

    if 'caption' not in kwargs or kwargs['caption'] == '':
        return operation_failed(InfoType.Needed, InfoField.Caption)
    caption = kwargs['caption']

    if database_exists(ProblemCategory, name=kwargs['name']):
        return operation_failed(InfoType.Exists, InfoField.Table.ProblemCategory)

    category = ProblemCategory(
        name=name,
        caption=caption,
    )

    if 'oj' in kwargs and kwargs['oj'] is not None:
        oj = database_get(OJ, name=kwargs['oj'])
        if oj is None:
            return operation_failed(InfoType.NotExists, InfoField.Table.OJ)
        category.oj = oj

    category.save()

    return operation_succeeded()


__category_create = []
__category_category_relation = []
__category_problem_relation = []

__problem_pid = dict()
__problem_index_pid = dict()

__generate_oj_category_error_info = None

__type_list = type(list())


def __generate_oj_category(oj, category_dict):
    global __category_create
    global __category_category_relation
    global __category_problem_relation

    global __problem_pid
    global __problem_index_pid

    global __generate_oj_category_error_info

    if 'name' not in category_dict:
        __generate_oj_category_error_info = operation_failed(InfoType.Needed, InfoField.Name)
        return False
    if 'caption' not in category_dict:
        __generate_oj_category_error_info = operation_failed(InfoType.Needed, InfoField.Caption)
        return False
    if 'child' not in category_dict:
        __generate_oj_category_error_info = operation_failed(
            InfoType.Needed, InfoField.Relation.ProblemCategoryChildren
        )
        return False

    if database_exists(ProblemCategory, name=category_dict['name']):
        __generate_oj_category_error_info = operation_failed(InfoType.Exists, InfoField.Table.ProblemCategory)
        return False

    category = ProblemCategory(
        name=category_dict['name'],
        caption=category_dict['caption'],
        oj=oj
    )
    __category_create.append(category)

    category_problems = set()

    if type(category_dict['child']) != __type_list:
        category_dict['child'] = [category_dict['child']]
    for cat in category_dict['child']:
        for child_type, child_dict in cat.items():
            if child_type == 'problem':
                if 'pid' in child_dict and child_dict['pid'] in __problem_pid:
                    problem = __problem_pid[child_dict['pid']]
                    relation = ProblemCategoryProblemRelation(
                        category=category,
                        problem=problem,
                        direct=True
                    )
                    __category_problem_relation.append(relation)
                    category_problems.add(problem)
                elif 'index_id' in child_dict and child_dict['index_id'] in __problem_index_pid:
                    problem = __problem_index_pid[child_dict['index_id']]
                    relation = ProblemCategoryProblemRelation(
                        category=category,
                        problem=problem,
                        direct=True
                    )
                    __category_problem_relation.append(relation)
                    category_problems.add(problem)
            if child_type == 'category':
                child_return = __generate_oj_category(oj, child_dict)
                if child_return is False:
                    return __generate_oj_category_error_info

                child_category = child_return['category']

                relation_category = ProblemCategoryCategoryRelation(
                    parent=category,
                    child=child_category
                )
                __category_category_relation.append(relation_category)

                child_problems = child_return['problem']

                for problem in child_problems:
                    relation_problem = ProblemCategoryProblemRelation(
                        category=category,
                        problem=problem,
                        direct=False,
                    )
                    __category_problem_relation.append(relation_problem)
                    category_problems.add(problem)

    return {
        'category': category,
        'problem': category_problems
    }


def create_oj_category(oj_name, category_dict):
    """
    传入根据目录生成的字典，生成指定OJ的目录
    :param oj_name: OJ的标识
    :param category_dict: 字典，包含目录信息：
        目录的格式为：
        {'name': 目录的name, 'caption': 目录的caption, 'child': 列表，可递归包含同样结构的目录以及题目}
        题目的格式为：
        {'pid': 题目的pid}或{'index_id': 题目的索引id}
    :return:
    """
    global __category_create
    global __category_category_relation
    global __category_problem_relation
    global __problem_pid
    global __problem_index_pid
    global __generate_oj_category_error_info

    oj = database_get(OJ, name=oj_name)
    if oj is None:
        return operation_failed(InfoType.NotExists, InfoField.Table.OJ)

    __category_create.clear()
    __category_category_relation.clear()
    __category_problem_relation.clear()

    __problem_pid.clear()
    __problem_index_pid.clear()

    problem_all = oj.problem.all()
    for problem in problem_all:
        __problem_pid[problem.pid] = __problem_index_pid[problem.index_id] = problem

    result = __generate_oj_category(oj, category_dict['category'])

    if result is False:
        return __generate_oj_category_error_info

    root_cat = database_get(ProblemCategory, name='root')

    __category_category_relation.append(ProblemCategoryCategoryRelation(
        parent=root_cat,
        child=result['category']
    ))
    for problem in __problem_pid.values():
        __category_problem_relation.append(
            ProblemCategoryProblemRelation(
                category=root_cat,
                problem=problem,
                direct=False
            )
        )

    ProblemCategory.objects.bulk_create(__category_create)
    ProblemCategoryCategoryRelation.objects.bulk_create(__category_category_relation)
    ProblemCategoryProblemRelation.objects.bulk_create(__category_problem_relation)

    return operation_succeeded()
