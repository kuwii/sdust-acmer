from django.conf.urls import url, include

urlpatterns = [
    url(r'^user/', include('api.urls.user')),
    url(r'^group/', include('api.urls.group')),
    url(r'^oj/', include('api.urls.oj')),
    url(r'^accounts/', include('api.urls.accounts')),
    url(r'^problems/', include('api.urls.problems')),
    url(r'^categories/', include('api.urls.categories')),
    url(r'^submissions/', include('api.urls.submissions')),
]
