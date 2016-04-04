from django.conf.urls import url

from front_end.views.submission import submission_ajax_page, submission_all_ajax_page


urlpatterns = [
    url(r'^get/(\S+)/(\d+)/(\d+)/', submission_ajax_page, name='submission_ajax'),
    url(r'^get/(\S+)/', submission_all_ajax_page, name='submission_all_ajax'),
]
