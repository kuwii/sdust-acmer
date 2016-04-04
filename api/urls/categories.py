from django.conf.urls import url

from ..views.categories import get_user_info

urlpatterns = [
    url(r'^get-user-info/(\S+)/', get_user_info, name='get_user_info'),
]
