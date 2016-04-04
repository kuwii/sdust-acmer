from django.conf.urls import url

from api.views.accounts import user_accounts_all
from api.views.accounts import create_account_post
from api.views.accounts import delete_account_post

urlpatterns = [
    url(r'^user-accounts/(\S+)/', user_accounts_all, name='user_accounts'),
    url(r'^create/', create_account_post, name='create-accounts'),
    url(r'^delete/', delete_account_post, name='delete-accounts'),
]
