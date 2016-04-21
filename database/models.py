from django.db import models
from django.contrib.auth.models import User


# OJ ------------------------------------------------------------------------------------------------------------------

class OJ(models.Model):
    """
    OJ信息。
    """
    name = models.CharField(max_length=8, unique=True)                  # OJ内部标识
    caption = models.CharField(max_length=64, default='--')             # OJ对外显示的名称
    available = models.BooleanField(default=False)                      # 该OJ是否可用

    notice = models.TextField(default='')                               # 该OJ对外公告

    crawler_problem = models.CharField(max_length=32, null=True)        # 该OJ题目信息函数
    crawler_submission = models.CharField(max_length=32, null=True)     # 该OJ提交记录的函数
    crawler_category = models.CharField(max_length=32, null=True)       # 该OJ更新提交记录的函数

    last_update_time = models.BigIntegerField(default=0)                # 该OJ上次更新题目信息的时间
    updating = models.BooleanField(default=False)                       # 该OJ当前是否在更新题目信息

    def __str__(self):
        return '<OJ: '+str(self.name)+'>'


class OJAccount(models.Model):
    """
    OJ帐号信息。
    """
    OJ = models.ForeignKey(OJ, to_field='name', related_name='account')             # 帐号所属OJ
    OJ_caption = models.CharField(max_length=64)                                    # OJ对外显示的名称
    user = models.ForeignKey(User, to_field='username', related_name='account')     # 帐号所属用户
    account = models.CharField(max_length=32)                                       # 帐号名

    def __str__(self):
        return '<OJ: '+str(self.OJ_id)+','+str(self.user_id)+','+str(self.account)+'>'


# User ----------------------------------------------------------------------------------------------------------------

class UserProfile(models.Model):
    """
    用户详细个人信息。
    """
    SEX_CHOICES = ['male', 'female', 'secret']

    user = models.OneToOneField(User, to_field='username', related_name='profile')  # 该信息所属用户

    username = models.CharField(max_length=30, unique=True)                         # 用户名，留出冗余便于提高查询效率
    register_time = models.BigIntegerField(default=0)                               # 用户注册时间

    nickname = models.CharField(null=True, max_length=64)                           # 昵称
    sex = models.CharField(null=False, max_length=8, default='secret')              # 性别
    photo = models.FileField(null=True, max_length=64)                              # 头像图片
    school = models.CharField(null=True, max_length=128)                            # 学校

    following = models.ManyToManyField(
        'self', related_name='followers',
        through='UserFollowingRelation', through_fields=('follower', 'following'),
        symmetrical=False
    )                                                                               # 关注的用户

    submission_number = models.IntegerField(default=0)                              # 提交记录数量

    problem_solved_number = models.IntegerField(default=0)                          # 通过的题目数量
    problem_tried_number = models.IntegerField(default=0)                           # 做过的题目数量

    last_update_time = models.BigIntegerField(default=0)                            # 该用户上次更新提交记录的时间
    updating = models.BooleanField(default=False)                                   # 该用户当前是否在更新提交记录

    def __str__(self):
        return '<OJ: '+str(self.user_id)+'>'


class UserFollowingRelation(models.Model):
    """
    用户之间相互关注的关系。
    """
    follower = models.ForeignKey(
        UserProfile, related_name='following_relation', to_field='user', on_delete=models.CASCADE
    )                                                                               # 关注者
    following = models.ForeignKey(
        UserProfile, related_name='follower_relation', to_field='username', on_delete=models.CASCADE
    )                                                                               # 关注的人


class UserStudent(models.Model):
    """
    内部训练时记录学生信息。
    """
    user = models.ForeignKey(User, to_field='username')                             # 该学生信息所属到用户

    school = models.CharField(max_length=16)                                        # 学校
    sno = models.CharField(max_length=16)                                           # 学号
    college = models.CharField(max_length=128)                                      # 学院
    major = models.CharField(max_length=128)                                        # 专业
    class_in = models.CharField(max_length=64)                                      # 班级


class UserIdentity(models.Model):
    """
    用户的身份信息。
    使用整数值代表权限，值为非0时代表具有权限，数值越大权限越小。
    安排为五个等级：
               0：失效，通常代表被管理员冻结，没有权限，无法登录。
             100：root，具有所有权限，最高等级用户。
             200：网站管理员，具有几乎所有权限，管理维护网站。
             300：用户管理员，具有大部分权限，管理用户组和用户
             400：普通用户，具有最基本的权限
    IDENTITY_CHOICES中为对应大等级权限值的下限。
    除失效用户和normal用户外，其他等级的用户均有权限管理等级比自己低的用户，修改用户信息，但无权将用户权限升至自己所在的大等级或之上。
    """
    IDENTITY_DIVISION = (
        (0, 'disabled'),
        (100, 'root'),
        (200, 'admin'),
        (300, 'manager'),
        (400, 'normal')
    )

    IDENTITY_WORD = dict(IDENTITY_DIVISION)
    IDENTITY_VALUE = dict(zip(IDENTITY_WORD.values(), IDENTITY_WORD.keys()))

    user = models.OneToOneField(User, to_field='username', related_name='identity')  # 身份信息所属用户
    level = models.IntegerField(default=400, choices=IDENTITY_DIVISION)              # 权限值整数

    def __str__(self):
        return '<UserIdentity: '+str(self.user_id)+', '+str(self.level)+'>'


class UserPermission(models.Model):
    """
    用户特定的权限信息。
    默认状态下用户拥有该用户所属等级用户到权限，当需要赋予某一等级用户超出用户等级的某一权限时，在此添加信息。
    """
    function = models.CharField(unique=True, max_length=32)                         # 动作名称
    explanation = models.TextField()                                                # 动作的详细解释
    user = models.ManyToManyField(
        User, related_name='permission',
        through='UserPermissionRelation', through_fields=('function', 'user')
    )                                                                               # 与此权限相关的用户


class UserPermissionRelation(models.Model):
    """
    用户特定权限信息与用户之间的关系。
    """
    user = models.ForeignKey(
        User, related_name='permission_relation',
        to_field='username', on_delete=models.CASCADE
    )
    function = models.ForeignKey(
        UserPermission, related_name='user_relation',
        to_field='function', on_delete=models.CASCADE
    )

    allowed = models.BooleanField()                                                 # 权限类型（是否允许执行）
    level = models.IntegerField(
        choices=UserIdentity.IDENTITY_DIVISION, default=UserIdentity.IDENTITY_VALUE['normal']
    )                         # 对于管理用户等需要结合被管理者权限等级判断是否有权限执行的动作，临时赋予管理者的权限等级


class UserGroup(models.Model):
    """
    用户组信息。
    用户组分为两种：
        0：公开群，所有人随意加入，无需申请。
        1：私有群，加入群需要申请，群管理员审核通过后方可加入。
    """
    name = models.CharField(unique=True, max_length=32)                             # 内部标识
    caption = models.CharField(max_length=64, default='')                           # 对外显示的名称
    public = models.BooleanField(default=False)                                     # 是否对外公开（任何人均可加入）
    register_time = models.BigIntegerField(null=False, default=0)                   # 创建时间

    member_number = models.IntegerField(default=0)                                  # 成员数量

    notice = models.TextField(default='')                                           # 公告
    introduction = models.TextField(default='')                                     # 介绍

    user = models.ManyToManyField(
        User, related_name='group',
        through='UserGroupRelation', through_fields=('group', 'user')
    )                                                                               # 组内包含的用户

    category = models.ManyToManyField(
        'ProblemCategory', related_name='group',
        through='ProblemCategoryGroupRelation', through_fields=('group', 'category')
    )                                                                               # 组内使用的统计目录


class UserGroupRelation(models.Model):
    """
    用户在用户组内的身份信息。
    用户在用户组内的身份分为五种：
        0：申请人。如果群为私有群的话，那么加入群需要管理员审核，在审核通过前身份为申请人。
        1：普通成员。
        2：管理员，审核申请，管理普通成员。
        3：boss，审核申请，管理所有群内成员。
    """
    user = models.ForeignKey(User, related_name='group_rel', to_field='username')       # 此身份所属用户，外键，指向用户名
    group = models.ForeignKey(UserGroup, related_name='user_rel', to_field='name')      # 此身份所在用户群，外键，指向群名

    identity = models.IntegerField(null=False, default=0)                               # 身份，限定的整数值


# Problem -------------------------------------------------------------------------------------------------------------

class Problem(models.Model):
    """
    题目信息
    """
    oj = models.ForeignKey(OJ, to_field='name', related_name='problem')             # 题目所属OJ
    oj_caption = models.CharField(max_length=64, default='')                        # OJ对外显示的名称

    pid = models.CharField(max_length=16, default='--')                             # 题目在原OJ上的编号
    index_id = models.CharField(max_length=32, unique=True)                         # 在数据库内查找时使用的标识

    title = models.CharField(max_length=128, default='--')                          # 题目标题
    available = models.BooleanField(default=False)                                  # 题目是否可用
    special_judge = models.BooleanField(default=False)                              # 是否是special judge

    time_limit = models.IntegerField(default=0)                                     # 题目的时间限制, ms
    memory_limit = models.IntegerField(default=-1)                                  # 题目的内存限制, k

    description = models.TextField(default='')                                      # 题意描述，暂不使用
    input = models.TextField(default='')                                            # 输入描述，暂不使用
    output = models.TextField(default='')                                           # 输出描述，暂不使用
    sample_input = models.TextField(default='')                                     # 示例输入，暂不使用
    sample_output = models.TextField(default='')                                    # 示例输出，暂不使用
    hint = models.TextField(default='')                                             # 提示，暂不使用
    source = models.TextField(default='Unknown')                                    # 来源，暂不使用

    judge = models.TextField(default='')                                            # 测试信息，暂不使用

    update_time = models.BigIntegerField(default=0)                                 # 更新时间，默认为0
    oj_special = models.TextField(default='')                                       # 该题目在原OJ上特有的其他字段

    user = models.ManyToManyField(
        User, related_name='problem_tried',
        through='ProblemUserRelation', through_fields=('problem', 'user')
    )                                                                               # 做过该题目的用户


class ProblemUserRelation(models.Model):
    """
    题目与做过的用户之间的关系。
    """
    user = models.ForeignKey(
        User, related_name='problem_tried_relation',
        to_field='username', on_delete=models.CASCADE
    )                                                                                   # 用户
    problem = models.ForeignKey(
        Problem, related_name='user_relation',
        to_field='id', on_delete=models.CASCADE
    )                                                                                   # 题目

    solved = models.BooleanField(default=False)                                         # 题目是否已经AC
    first_time = models.BigIntegerField(default=0)                                      # 第一次尝试该题目的时间
    ac_time = models.BigIntegerField(default=-1)                                        # AC时间


class Submission(models.Model):
    """
    提交记录。
    """
    user = models.ForeignKey(User, to_field='username', related_name='submission')          # 提交记录所属的用户
    account = models.ForeignKey(OJAccount, related_name='submission')                       # 提交记录所属的OJ帐号
    account_account = models.CharField(max_length=32)                                       # 帐号名

    oj = models.ForeignKey(OJ, to_field='name', related_name='submission')                  # 提交记录所属OJ
    oj_caption = models.CharField(max_length=64, default='')                                # OJ对外显示的名称

    problem = models.ForeignKey(Problem, to_field='id', related_name='submission')          # 提交记录所属题目
    problem_pid = models.CharField(max_length=16, default='--')                             # 题目在原OJ上的编号
    problem_title = models.CharField(max_length=128, default='--')                          # 题目标题
    problem_time_limit = models.IntegerField(default=0)                                     # 题目的时间限制
    problem_memory_limit = models.IntegerField(default=-1)                                  # 题目的内存限制

    sid = models.CharField(max_length=16, default='--')                                     # 提交记录在原OJ的编号

    sub_time = models.BigIntegerField(default=0)                                            # 提交时间
    result = models.CharField(max_length=32)                                                # 结果
    result_word = models.CharField(max_length=32)                                           # OJ本身的结果
    language = models.CharField(max_length=32, default='unknown')                           # 语言
    run_time = models.IntegerField(default=-1)                                              # 运行时间
    run_memory = models.IntegerField(default=-1)                                            # 运行内存，KB
    length = models.IntegerField(default=-1)                                                # 代码长度，B

    oj_special = models.TextField(null=False, default='')                                # 提交记录在原OJ上其他OJ特有的字段


class SubmissionResult(models.Model):
    """
    原OJ提交记录的结果与本系统提交记录结果的映射。
    """
    oj = models.ForeignKey(OJ, to_field='name', related_name='submission_result')           # 映射关系所属到OJ
    oj_result = models.CharField(max_length=64, null=False)                                 # 原OJ的提交记录结果
    result = models.CharField(max_length=64)                                                # 对应到提交记录结果


class ProblemCategory(models.Model):
    """
    题目的目录划分。
    """
    name = models.CharField(max_length=128, unique=True)                                         # 目录标识
    caption = models.CharField(max_length=128)                                                   # 目录对外显示的名称

    oj = models.ForeignKey(OJ, to_field='name', null=True, on_delete=models.CASCADE)             # 目录所属的OJ

    problem = models.ManyToManyField(
        Problem, related_name='category',
        through='ProblemCategoryProblemRelation', through_fields=('category', 'problem')
    )                                                                                 # 该目录下的所有问题，包括子结点

    category = models.ManyToManyField(
        'self', related_name='parent', symmetrical=False,
        through='ProblemCategoryCategoryRelation', through_fields=('parent', 'child')
    )                                                                                 # 该目录的子目录


class ProblemCategoryGroupRelation(models.Model):
    """
    目录划分与用户组之间的关系。
    """
    category = models.ForeignKey(ProblemCategory, to_field='name', on_delete=models.CASCADE)
    group = models.ForeignKey(UserGroup, to_field='name', on_delete=models.CASCADE)


class ProblemCategoryProblemRelation(models.Model):
    """
    目录划分与题目之间的关系。
    """
    category = models.ForeignKey(
        ProblemCategory, related_name='problem_relation',
        to_field='name', on_delete=models.CASCADE
    )
    problem = models.ForeignKey(
        Problem, related_name='category_relation',
        to_field='id', on_delete=models.CASCADE
    )

    direct = models.BooleanField(default=False)


class ProblemCategoryCategoryRelation(models.Model):
    """
    目录划分与子目录划分之间的关系。
    """
    parent = models.ForeignKey(
        ProblemCategory, related_name='category_relation',
        to_field='name', on_delete=models.CASCADE
    )
    child = models.ForeignKey(
        ProblemCategory, related_name='parent_relation',
        to_field='name', on_delete=models.CASCADE
    )
