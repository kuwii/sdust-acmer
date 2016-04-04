class GlobalValues:
    query_limit = 233


def first_one(table, **kwargs):
    """
    获取指定表的QuerySet中的第一个对象。
    :param table: 表
    :param kwargs: 包含查询关键字及值的字典
    :return: 如果QuerySet中有对象，返回包含第一个对象，否则返回None
    """
    return table.objects.filter(**kwargs).first()


def to_dict(element):
    """
    以字典的形式返回指定的QuerySet中某个对象的副本。
    :param element:
    :return:
    """
    if element is None:
        return None
    ret = vars(element)
    ret.pop('_state')
    return ret


def to_list(ret, get_all=False, start=0, end=GlobalValues.query_limit, values=list()):
    """
    将指定QuerySet转换为列表。
    :param ret: 指定QuerySet
    :param get_all: 是否取切片
    :param start: 查询结果切片的起点
    :param end: 查询结果切片的终点
    :param values: 查询结果切片的终点
    :return: 转换后的列表，列表中的对象均为字典对象
    """
    if ret is None:
        return {'length': 0, 'slice': []}

    length = ret.count()

    if end > length:
        end = length
    if start > length:
        start = length
    if start > end:
        start = end

    if get_all:
        ls = ret
    else:
        ls = ret[start: end]

    return {'length': length, 'slice': list(ls.values(*values))}
