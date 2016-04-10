from django.conf.urls import url

from ..views.categories import get_user_info, get_users_info

urlpatterns = [
    url(r'^get-user-info/(\S+)/', get_user_info, name='get_user_info'),
    url(r'^get-users-info/(\S+)/', get_users_info, name='get_users_info'),
]
