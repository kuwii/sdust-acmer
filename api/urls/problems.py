from django.conf.urls import url

from api.views.problems import update_problems_post

urlpatterns = [
    url(r'^update/', update_problems_post, name='update_problems'),
]
