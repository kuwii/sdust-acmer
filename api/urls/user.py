from django.conf.urls import url

from api.views.user import current_user, current_user_info
from api.views.user import get_user_info
from api.views.user import search_user_username, search_user_nickname
from api.views.user import create_user_post, login_post, logout
from api.views.user import modify_user_info_post, change_password_post
from api.views.user import follow_user_post, unfollow_user_post

urlpatterns = [
    url(r'^current-user/', current_user, name='current_user'),
    url(r'^current-user-info/', current_user_info, name='current_user_info'),

    url(r'^get-user-info/(\S+)/', get_user_info, name='get_user_info'),
    url(r'^search-user-username/(\S+)/', search_user_username, name='search_user'),
    url(r'^search-user-nickname/(\S+)/', search_user_nickname, name='search_user'),

    url(r'^register/', create_user_post, name='register'),
    url(r'^login/', login_post, name='login'),
    url(r'^logout/', logout, name='logout'),

    url(r'^modify/', modify_user_info_post, name='modify'),
    url(r'^change-password/', change_password_post, name='change_password'),

    url(r'^follow/', follow_user_post, name='follow_user'),
    url(r'^unfollow/', unfollow_user_post, name='unfollow_user'),
]
