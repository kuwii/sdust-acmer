from database.models import OJ

from database.query.util import to_list, first_one, to_dict
from database.query.util import GlobalValues


QueryLimit = GlobalValues.query_limit


def oj_all():
    """
    返回所有OJ的信息。
    :return: 所有OJ，列表
    """
    return to_list(OJ.objects.all(), get_all=True)


def get_oj(name):
    """
    获取指定OJ信息。
    :param name: OJ的标识
    :return: 如果OJ存在，返回包含OJ信息的字典，否则返回None
    """
    ret = first_one(OJ, name=name)
    return to_dict(ret)


def search_oj(name=None, caption=None, start=0, end=QueryLimit):
    """
    搜索OJ。
    :param name: OJ标识，默认按照name搜索
    :param caption: OJ名称，此项不为None则按照OJ名称搜索
    :param start: 查询结果切片的起点
    :param end: 查询结果切片的终点
    :return: 搜索结果，列表
    """
    if name is None and caption is None:
        return []

    ret = OJ.objects

    if name is not None:
        ret = ret.filter(name__contains=name)
    if caption is not None:
        ret = ret.filter(caption__contains=caption)

    return to_list(ret, start=start, end=end)


def oj_updating(oj_name):
    """
    查询OJ是否在更新状态。
    :param oj_name:
    :return:
    """
    oj = first_one(OJ, name=oj_name)
    if oj is None:
        return None
    return oj.updating
