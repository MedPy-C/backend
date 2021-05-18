from django.urls import path

from backoffice.view import user_login

user_login_routes = [
    path('signup/', user_login.UserLoginView.as_view(
        {'post': 'create'}), name='signup'),
    path('users/list/', user_login.UserLoginView.as_view(
        {'get': 'list'}), name='list_all_users')
]
