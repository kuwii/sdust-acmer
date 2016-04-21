import crawler.function.UVa as __CrawlerUVa
import crawler.function.POJ as __CrawlerPOJ


__crawler_problems_entry = {
    'UVA_PROBLEMS': __CrawlerUVa.get_problems,
    'POJ_PROBLEMS': __CrawlerPOJ.get_problems
}

__crawler_submissions_entry = {
    'UVA_SUBMISSIONS': __CrawlerUVa.get_submissions,
    'POJ_SUBMISSIONS': __CrawlerPOJ.get_submissions
}

__crawler_categories_entry = {
    'UVA_CATEGORIES': __CrawlerUVa.get_uva_category,
    'POJ_CATEGORIES': __CrawlerPOJ.get_categories
}


def get_problems(crawler_name):
    if crawler_name not in __crawler_problems_entry:
        return None
    return __crawler_problems_entry[crawler_name]()


def get_submissions(crawler_name, account):
    if crawler_name not in __crawler_submissions_entry:
        return None
    return __crawler_submissions_entry[crawler_name](account)


def get_categories(crawler_name):
    if crawler_name not in __crawler_categories_entry:
        return None
    return __crawler_categories_entry[crawler_name]()
