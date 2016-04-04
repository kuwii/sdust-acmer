from django.conf.urls import url

from api.views.submission import update_submission_post

urlpatterns = [
    url(r'^update/', update_submission_post, name='update_submissions'),
]
