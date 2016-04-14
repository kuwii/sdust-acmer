from django.conf.urls import url

from front_end.views.group import search_group, group_info
from front_end.views.group import edit_group


urlpatterns = [
    url(r'^search/(\S+)/(\d+)/(\d+)/', search_group, name='search_group'),
    url(r'^info/(\S+)/', group_info, name='group_info'),
    url(r'^edit/(\S+)/', edit_group, name='edit_group'),
]
