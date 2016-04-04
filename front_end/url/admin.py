from django.conf.urls import url

from front_end.views.admin import admin_page, new_oj, edit_oj, upload_xml


urlpatterns = [
    url(r'^site-admin/', admin_page, name='site-admin'),
    url(r'^new-oj/', new_oj, name='new-oj'),
    url(r'^edit-oj/(\S+)/', edit_oj, name='edit-oj'),
    url(r'^upload-xml/(\S+)/', upload_xml, name='upload-xml'),
]
