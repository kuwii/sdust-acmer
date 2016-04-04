import json
import time
import xml.etree.ElementTree

from lxml import etree as __etree

from .util import get_page as __get_page


# Utility --------------------------------------------------------------------------------------------------------------

__uhunt_id_url = 'http://uhunt.felix-halim.net/api/uname2uid/'
__uhunt_problem_url = 'http://uhunt.felix-halim.net/api/p'
__uhunt_submission_url = 'http://uhunt.felix-halim.net/api/subs-user/'

__verdict_id = {
    10: 'Submission error',
    15: 'Can\'t be judged',
    20: 'In queue',
    30: 'Compile error',
    35: 'Restricted function',
    40: 'Runtime error',
    45: 'Output limit',
    50: 'Time limit',
    60: 'Memory limit',
    70: 'Wrong answer',
    80: 'PresentationE',
    90: 'Accepted'
}

__language_id = {
    1: 'ANSI C',
    2: 'java',
    3: 'C++',
    4: 'Pascal',
    5: 'C++11',
}


class Category:
    def __init__(self, **kwargs):
        self.name = kwargs['name'] if 'name' in kwargs else 'uva'
        self.caption = kwargs['caption'] if 'caption' in kwargs else ''

        self.problem = kwargs['problem'] if 'problem' in kwargs else list()
        self.category = kwargs['category'] if 'category' in kwargs else list()

    def __str__(self):
        return '<Category: ' + self.name + ', ' + self.caption + '>'


def __get_uhunt_id(account):
    return __get_page(__uhunt_id_url + account)


def __get_user_submission_url(account):
    uid = __get_uhunt_id(account)
    if uid is False:
        return False
    return __uhunt_submission_url + uid


# Function -------------------------------------------------------------------------------------------------------------

def get_submissions(account):
    """
    获取指定用户的提交记录。
    :param account: 用户在UVa上的帐户名
    :return: 提交记录，列表
    """
    url = __get_user_submission_url(account)
    if url is False:
        return False

    page = __get_page(url)
    if page is False:
        return False

    data = json.loads(page)
    data_subs = data['subs']

    subs = []
    for sub in data_subs:
        subs.append({
            'solved': True if sub[2] == 90 else False,

            'sid': str(sub[0]),
            'index_id': 'uva'+str(sub[1]),
            'result': __verdict_id[sub[2]],
            'run_time': sub[3],
            'sub_time': sub[4],
            'language': __language_id[sub[5]],
            'oj_special': json.dumps({
                'Submission Rank': sub[6]}
            )
        })

    return subs


def get_problems():
    """
    获取UVa上的所有题目信息。
    :return: 题目信息，列表
    """
    page = __get_page(__uhunt_problem_url)
    if page is False:
        return False

    data_problems = json.loads(page)

    problems = []
    for problem in data_problems:
        problems.append({
            'pid': str(problem[1]),
            'index_id': 'uva'+str(problem[0]),
            'title': problem[2],
            'available': True if problem[20] != 0 else False,
            'special_judge': True if problem[20] == 2 else False,
            'time_limit': int(problem[19]),
            'update_time': int(time.time()),
            'oj_special': json.dumps({
                'Number of Distinct Accepted User': problem[3],
                'Best Runtime of an Accepted Submission': problem[4],
                'Best Memory used of an Accepted Submission': problem[5],
                'Number of No Verdict Given': problem[6],
                'Number of Submission Error': problem[7],
                'Number of Can\'t be Judged ': problem[8],
                'Number of In Queue ': problem[9],
                'Number of Compilation Error': problem[10],
                'Number of Restricted Function': problem[11],
                'Number of Runtime Error': problem[12],
                'Number of Output Limit Exceeded': problem[13],
                'Number of Time Limit Exceeded': problem[14],
                'Number of Memory Limit Exceeded': problem[15],
                'Number of Wrong Answer': problem[16],
                'Number of Presentation Error': problem[17],
                'Number of Accepted': problem[18]
            })
        })

    return problems


def __generate_uva_category(
        category=Category(),
        url='https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8'
):
    print('Crawling: ' + url)
    page = __get_page(url)
    data = __etree.HTML(page)

    cat_no = 0

    items = data.xpath(
        r"//div[@id='col3_content_wrapper']/table/tr[@class='sectiontableentry1' or @class='sectiontableentry2']"
    )

    for item in items:
        item_name = item.xpath(r"td[3]/a/text()")[0]
        item_url = str(item.xpath("td[3]/a/@href")[0])

        if len(item.xpath("td[4]/text()")) == 0:
            cat = (
                Category(name=category.name+'-'+str(cat_no), caption=item_name),
                'https://uva.onlinejudge.org/' + item_url
            )
            category.category.append(cat)
            cat_no += 1
            print('Category Found: ' + str(cat[0]))
        else:
            pid = ""
            for i in item_name:
                if i.isdigit():
                    pid += i
                else:
                    break
            category.problem.append(pid)
            print('Problem Found: ' + item_name)

    for i in category.category:
        __generate_uva_category(category=i[0], url=i[1])

    return category


def __category_to_dict(category):
    cat = {
        'name': category.name,
        'caption': category.caption,
        'child': list()
    }
    for i in category.category:
        cat['child'].append(__category_to_dict(i[0]))
    for i in category.problem:
        cat['child'].append({
            'problem': {
                'pid': i
            }
        })

    return {
        'category': cat
    }


def get_uva_category():
    return __category_to_dict(__generate_uva_category())
