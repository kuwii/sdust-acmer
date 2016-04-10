class InfoType:
    Null = 'NULL'
    Unknown = 'UNKNOWN'
    Exists = 'EXISTS'
    NotExists = 'NOT_EXISTS'
    Needed = 'NEEDED'
    Wrong = 'WRONG'
    Value = 'VALUE'
    Invalid = 'INVALID'
    Updating = 'UPDATING'


class InfoField:
    Null = 'NULL'
    Unknown = 'UNKNOWN'

    OJ = 'OJ'
    User = 'USER'
    UserFollowingRelation = 'USER_FOLLOWING_RELATION'

    Caption = 'CAPTION'
    IdentityWord = 'IDENTITY_WORD'
    Name = 'NAME'
    Password = 'PASSWORD'
    UserSex = 'USER_SEX'
    Username = 'USERNAME'

    class Table:
        OJ = 'OJ'
        User = 'USER'
        UserGroup = 'USER_GROUP'
        Account = 'ACCOUNT'
        ProblemCategory = 'CATEGORY'

    class Relation:
        UserGroupRelation = 'USER_GROUP_RELATION'
        ProblemCategoryChildren = 'CATEGORY_CHILDREN'


class ResultInfo:
    def __init__(self, info_type=InfoType.Unknown, info_field=InfoField.Unknown):
        self.info_type = info_type
        self.info_field = info_field

    def __str__(self):
        return str((self.info_type, self.info_field))


class OperationResult:
    def __init__(self, ok=False, info=ResultInfo(InfoType.Unknown, InfoField.Unknown)):
        self.ok = ok
        self.info = info

    def __str__(self):
        return str((self.ok, str(self.info)))


def operation_failed(info_type, info_field):
    return OperationResult(False, ResultInfo(info_type, info_field))


def operation_succeeded():
    return OperationResult(True, ResultInfo(InfoType.Null, InfoField.Null))


def database_get(table, **kwargs):
    return table.objects.filter(**kwargs).first()


def database_exists(table, **kwargs):
    return table.objects.filter(**kwargs).exists()
