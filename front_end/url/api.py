from django.conf.urls import url

from front_end.views.api import api_index


urlpatterns = [
    url(r'^index/', api_index, name='api_index'),
]
