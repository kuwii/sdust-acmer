"""SDUST_ACMER URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from front_end.views.basic import to_home, homepage
from front_end.views.basic import faq

urlpatterns = [
    url(r'^$', to_home, name='to_home'),

    url(r'^home/', homepage, name='homepage'),
    url(r'^faq/', faq, name='faq'),

    url(r'^user/', include('front_end.url.user')),
    url(r'^group/', include('front_end.url.group')),

    url(r'^admin/', include('front_end.url.admin')),
    url(r'^manager/', include('front_end.url.manager')),

    url(r'^api/', include('api.urls.index')),

    url(r'^api-help/', include('front_end.url.api')),
]
