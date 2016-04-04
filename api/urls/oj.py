from django.conf.urls import url

from api.views.oj import create_oj_post, modify_oj_post, delete_oj_post

urlpatterns = [
    url(r'^create/', create_oj_post, name='create_oj'),
    url(r'^modify/', modify_oj_post, name='modify_oj'),
    url(r'^delete/', delete_oj_post, name='delete_oj'),
]
