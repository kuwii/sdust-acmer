from django.conf.urls import url

from front_end.views.category import category_ajax_page


urlpatterns = [
    url(r'^get/(\S+)/', category_ajax_page, name='category_all_ajax'),
]
