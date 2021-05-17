from django.urls import path

from backoffice.view import user_login

user_login_routes = [
    path('users_login/', user_login.UserLoginView.as_view(
        {'post': 'create',
         'get': 'list'}), name='refresh')
]
