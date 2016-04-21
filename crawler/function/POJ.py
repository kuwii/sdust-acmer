import time
import json

from lxml import etree as _etree
from .util import get_page as _util_get_page


# Util -----------------------------------------------------------------------------------------------------------------

class POJCrawler:

    _poj_url = 'http://poj.org/'
    _poj_volume_root_url = 'http://poj.org/problemlist?volume=1'
    _poj_user_url = 'http://poj.org/status?user_id='

    def __init__(self):
        self._problem_urls = []
        self._volume_urls = []

        self.submissions = []
        self.problems = []
        self.volumes = []

        self._time_limit = 0

        self._poj_time_format = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def _get_number(num_str):
        """
        将指定字符串中的数字提取出来
        :param num_str: 包含数字的字符串
        :return: 提取出的整数
        """
        t_str = ''
        for c in num_str:
            if c.isdigit():
                t_str += c
        if len(t_str) == 0:
            return 0
        else:
            return int(t_str)

    @staticmethod
    def _get_page(url):
        """
        获取指定网页的HTML代码
        :param url: 网址
        :return: 整个页面的HTML代码
        """
        return _util_get_page(url)

    def _crawl_volume_urls(self):
        """
        从POJ上获取所有目录的链接，保存在_volume_urls中
        :return: 无
        """
        # 一点点清理工作
        self._volume_urls.clear()

        # 获取网页HTML代码
        url = POJCrawler._poj_volume_root_url
        page = self._get_page(url)
        if page is not False:
            # 分析HTML代码，提取出所有目录的链接
            data = _etree.HTML(page)
            volumes = data.xpath(
                r"/html/body/center/a/@href"
            )
            # 将所有目录的链接存入_volume_urls中
            for volume_url in volumes:
                self._volume_urls.append(volume_url)

    def _crawl_problem_urls(self, url):
        """
        从指定目录的url对应的网页上获取所有该目录下的题目链接和基本题目信息，保存在_problem_urls中
        :param url: 目录的超链接
        :return: 无
        """
        # 一点点清理工作
        self._problem_urls.clear()
        problem_url = self._poj_url + url
        page = self._get_page(problem_url)
        if page is not False:
            # 分析HTML代码，提取出所有题目
            data = _etree.HTML(page)
            problems = data.xpath(
                r"/html/body/table[2]/tr[@align='center']"
            )
            # 将题目链接及基本题目信息存入_problem_urls中
            for problem in problems:
                pid = problem.xpath(r"td[1]/text()")[0]
                index_id = 'poj'+pid
                title = problem.xpath(r"td[2]/a/text()")[0]
                p_link = problem.xpath(r"td[2]/a/@href")[0]
                self._problem_urls.append((pid, index_id, title, p_link))

    def _crawl_problem_info(self, info):
        """
        获取指定题目信息，将题目信息存入problems中
        :param info: 题目信息，由_crawl_problem_urls生成
        :return: 无
        """
        problem_url = self._poj_url + info[3]
        page = self._get_page(problem_url)
        if page is not False:
            print(page)
            data = _etree.HTML(page)
            prob_basic_info = data.xpath(
                r"//div[@class='plm']/table"
            )[0]
            time_limit = self._get_number(prob_basic_info.xpath(r"tr[1]/td[1]/text()")[0])
            memory_limit = self._get_number(prob_basic_info.xpath(r"tr[1]/td[3]/text()")[0])
            total_submissions = self._get_number(prob_basic_info.xpath(r"tr[2]/td[1]/text()")[0])
            accepted = self._get_number(prob_basic_info.xpath(r"tr[2]/td[3]/text()")[0])

            problem_info = {
                'pid': info[0],
                'index_id': info[1],
                'title': info[2],
                'available': True,
                'time_limit': time_limit,
                'memory_limit': memory_limit,
                'update_time': int(time.time()),
                'oj_special': json.dumps({
                    'total_submissions': total_submissions,
                    'accepted': accepted
                })
            }
            self.problems.append(problem_info)
            print('problem get :', info)

    def get_submissions(self, uid):
        """
        从POJ上下载所有提交记录信息
        :param uid: 用户的id
        :return: 所有提交记录信息，列表形式
        """
        self._time_limit = 1
        page = self._get_page(self._poj_user_url + uid)
        if page is None:
            return
        while True:
            data = _etree.HTML(page)
            next_link = self._poj_url + data.xpath(r"/html/body/p[2]/a[3]/@href")[0]
            submissions = data.xpath(r"/html/body/table[2]/tr[@align='center']")
            has_submission = True if len(submissions) > 0 else False
            for submission in submissions:
                sid = submission.xpath(r"td[1]/text()")[0]
                index_id = 'poj'+submission.xpath(r"td[3]/a/text()")[0]

                result = submission.xpath(r"td[4]/font/text()")
                if len(result) == 0:
                    result = submission.xpath(r"td[4]/a/font/text()")[0]
                else:
                    result = result[0]

                solved = True if result == 'Accepted' else False
                run_time = submission.xpath(r"td[6]/text()")
                run_memory = submission.xpath(r"td[5]/text()")
                language = submission.xpath(r"td[7]/text()")[0]
                length = self._get_number(submission.xpath(r"td[8]/text()")[0])
                sub_time = int(time.mktime(time.strptime(submission.xpath(r"td[9]/text()")[0], self._poj_time_format)))

                sub = {
                    'sid': sid,
                    'index_id': index_id,
                    'result': result,
                    'solved': solved,
                    'language': language,
                    'length': length,
                    'sub_time': sub_time
                }
                if len(run_time) == 1:
                    sub['run_time'] = self._get_number(run_time[0])
                if len(run_memory) == 1:
                    sub['run_memory'] = self._get_number(run_memory[0])

                print(sub)
                self.submissions.append(sub)
            if has_submission:
                time.sleep(self._time_limit)
                page = self._get_page(next_link)
                if page is None:
                    break
            else:
                break

    def get_problems(self):
        """
        从POJ上下载所有题目信息。
        :return: 所有题目信息，列表形式
        """
        # 一点点清理工作
        self.problems.clear()
        self.volumes.clear()

        # 获得所有目录的链接
        self._crawl_volume_urls()
        print('%d volumes got' % len(self._volume_urls))

        # 解析每个目录，分析所有题目的链接
        self._time_limit = 0.3
        for url in self._volume_urls:
            self._crawl_problem_urls(url)
            time.sleep(self._time_limit)
        print('%d problems got' % len(self._problem_urls))

        # 解析每个题目，获得题目信息
        self._time_limit = 6
        for url in self._problem_urls:
            self._crawl_problem_info(url)
            time.sleep(self._time_limit)

        return self.problems


# Function -------------------------------------------------------------------------------------------------------------

def get_problems():
    poj = POJCrawler()
    return poj.get_problems()


def get_submissions(account):
    poj = POJCrawler()
    return poj.get_submissions(account)


def get_categories():
    return {}
