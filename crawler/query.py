import crawler.function.UVa as __crawler_uva


__crawler_problems_entry = {
    'UVA_PROBLEMS': __crawler_uva.get_problems
}

__crawler_submissions_entry = {
    'UVA_SUBMISSIONS': __crawler_uva.get_submissions
}

__crawler_categories_entry = {
    'UVA_CATEGORIES': __crawler_uva.get_uva_category
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
