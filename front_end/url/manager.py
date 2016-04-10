from django.conf.urls import url

from front_end.views.manager import manager_page


urlpatterns = [
    url(r'^site-manager/', manager_page, name='site-manager'),
]
