from database.models import OJ

from .util import InfoType, InfoField
from .util import operation_succeeded, operation_failed


def create_oj(**kwargs):
    """
    创建OJ。
    :param kwargs:
    :return:
    """
    if 'name' not in kwargs or kwargs['name'] == '':
        return operation_failed(InfoType.Needed, InfoField.Name)
    name = kwargs['name'].lower()

    if 'caption' not in kwargs or kwargs['caption'] == '':
        return operation_failed(InfoType.Needed, InfoField.Name)

    if OJ.objects.filter(name=name).exists():
        return operation_failed(InfoType.Exists, InfoField.OJ)

    oj = OJ(
        name=name, caption=kwargs['caption'],
        available=kwargs['available'] if 'available' in kwargs else False,
        notice=kwargs['notice'] if 'notice' in kwargs else '',
        crawler_problem=kwargs['crawler_problem'] if 'crawler_problem' in kwargs else None,
        crawler_submission=kwargs['crawler_submission'] if 'crawler_submission' in kwargs else None,
        crawler_category=kwargs['crawler_category'] if 'crawler_category' in kwargs else None,
        updating=False,
    )
    oj.save()

    return operation_succeeded()


def modify_oj(**kwargs):
    """
    修改OJ信息。
    :param kwargs:
    :return:
    """
    if 'name' not in kwargs:
        return operation_failed(InfoType.Needed, InfoField.Name)
    name = kwargs['name'].lower()

    if 'caption' not in kwargs or kwargs['caption'] == '':
        return operation_failed(InfoType.Wrong, InfoField.Caption)

    oj = OJ.objects.filter(name=name).first()
    if oj is None:
        return operation_failed(InfoType.NotExists, InfoField.OJ)

    if 'caption' in kwargs:
        oj.caption = kwargs['caption']
    if 'available' in kwargs:
        oj.available = kwargs['available']
    if 'notice' in kwargs:
        oj.notice = kwargs['notice'] if kwargs['notice'] != '' else None
    if 'crawler_problem' in kwargs:
        oj.crawler_problem = kwargs['crawler_problem'] if kwargs['crawler_problem'] != '' else None
    if 'crawler_submission' in kwargs:
        oj.crawler_submission = kwargs['crawler_submission'] if kwargs['crawler_submission'] != '' else None
    if 'crawler_crawler' in kwargs:
        oj.crawler_category = kwargs['crawler_category'] if kwargs['crawler_category'] != '' else None

    oj.account.all().update(OJ_caption=oj.caption)
    oj.problem.all().update(oj_caption=oj.caption)
    oj.submission.all().update(oj_caption=oj.caption)

    oj.save()

    return operation_succeeded()


def delete_oj(oj_name):
    """
    删除指定OJ。
    :param oj_name: OJ的name项
    :return: 操作结果
    """
    oj = OJ.objects.filter(name=oj_name).first()
    if oj is None:
        return operation_failed(InfoType.NotExists, InfoField.OJ)

    oj.delete()

    return operation_succeeded()
