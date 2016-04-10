from django.conf.urls import url, include

from front_end.views.user import sign_in, sign_up, settings
from front_end.views.user import training_information
from front_end.views.user import search_user
from front_end.views.user import following_followers

from front_end.views.user import user_group


urlpatterns = [
    url(r'^login/', sign_in, name='sign_in'),
    url(r'^register/', sign_up, name='sign_up'),
    url(r'^settings/(\S+)/', settings, name='user_settings'),

    url(r'^info/(\S+)/', training_information, name='user_training_info'),
    url(r'^follow/(\S+)/', following_followers, name='following_followers'),
    url(r'^group/(\S+)/', user_group, name='user_group'),

    url(r'^search/(\S+)/(\d+)/(\d+)/', search_user, name='search_user'),

    url(r'^submissions/', include('front_end.url.submissions')),
    url(r'^problems/', include('front_end.url.problems')),
    url(r'^categories/', include('front_end.url.categories')),
]
