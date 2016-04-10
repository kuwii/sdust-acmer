from django.conf.urls import url

from ..views.groups import get_group, get_group_user, search_group
from ..views.groups import create_group_post, modify_group_post, delete_group_post

from ..views.groups import join_group_post

urlpatterns = [
    url(r'^get/(\S+)/', get_group, name='get_group'),
    url(r'^get-user/(\S+)/', get_group_user, name='get_group_user'),
    url(r'^search/(\S+)/', search_group, name='search_group'),

    url(r'^create/', create_group_post, name='create_group'),
    url(r'^modify/', modify_group_post, name='modify_group'),
    url(r'^delete/', delete_group_post, name='delete_group'),

    url(r'^join/', join_group_post, name='join_group'),
]
