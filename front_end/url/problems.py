from django.conf.urls import url

from front_end.views.problem import problem_ajax_page, problem_all_ajax_page


urlpatterns = [
    url(r'^get/(\S+)/(\d+)/(\d+)/', problem_ajax_page, name='problem_ajax'),
    url(r'^get/(\S+)/', problem_all_ajax_page, name='problem_all_ajax'),
]
