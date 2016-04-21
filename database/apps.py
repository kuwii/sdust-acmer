from django.apps import AppConfig
from django.db.models.signals import post_migrate


def __check_root_user():
    """
    检查初始root用户是否存在，如不存在则创建初始用户。
    :return: 无
    """
    from .models import User
    print('Checking Initial User ...', end='')
    if User.objects.filter(username='korosensei').exists():
        print(' OK')
    else:
        print(' Not Exists ...           ', end='')
        print('Creating ...', end='')
        from database.function.user import create_user
        create_user('korosensei', 'big_boss', 'root')
        print(' Done')


def __check_root_category():
    """
    检查初始根目录，如不存在则创建根目录。
    :return: 无
    """
    from .models import ProblemCategory
    print('Checking Initial Category ...', end='')
    if ProblemCategory.objects.filter(name='root').exists():
        print(' OK')
    else:
        print(' Not Exists ... ', end='')
        print('Creating ...', end='')
        from database.function.category import create_category
        create_category(
            name='root',
            caption='Root',
            oj=None
        )
        print(' Done')


def __check_oj_uva():
    """
    初始化UVa的OJ表。
    :return: 无
    """
    from .models import OJ
    print('Checking Uva ...', end='')
    if OJ.objects.filter(name='uva').exists():
        print(' OK')
    else:
        print(' Not Exists ... ', end='')
        print('Creating ...', end='')
        from database.function.oj import create_oj
        create_oj(
            name='uva',
            caption='UVa Online Judge',
            available=True,
            crawler_problem='UVA_PROBLEMS',
            crawler_submission='UVA_SUBMISSIONS',
            crawler_category='UVA_CATEGORIES'
        )
        print(' Done')
    print('Checking POJ ...', end='')
    if OJ.objects.filter(name='poj').exists():
        print(' OK')
    else:
        print(' Not Exists ... ', end='')
        print('Creating ...', end='')
        from database.function.oj import create_oj
        create_oj(
            name='poj',
            caption='PKU JudgeOnline',
            available=True,
            crawler_problem='POJ_PROBLEMS',
            crawler_submission='POJ_SUBMISSIONS',
            crawler_category='POJ_CATEGORIES'
        )
        print(' Done')


def my_callback(sender, **kwargs):
    print('')
    print('#########################')
    print('#         ACMer         #')
    print('#########################')
    print('')
    print('Database Initialization:')
    __check_root_user()
    __check_root_category()
    __check_oj_uva()


class DatabaseConfig(AppConfig):
    name = 'database'

    def ready(self):
        post_migrate.connect(my_callback, sender=self)
