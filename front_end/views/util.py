from database.query.permission import get_identity_map


def has_login(request):
    return request.user.is_authenticated()


def user_status(request):
    if has_login(request):
        info = request.user.profile
        return {
            'authenticated': True,
            'nickname': info.nickname if info.nickname else info.username,
            'username': info.username,
            'identity': get_identity_map(request.user.username)
        }
    else:
        return {'authenticated': False}
