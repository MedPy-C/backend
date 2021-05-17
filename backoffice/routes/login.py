from django.urls import path

from backoffice.view import login

login_routes = [
    path('login/', login.LoginViewSet.as_view({'post': 'authenticate'}), name='authentication'),
    path('login/refresh/', login.LoginViewSet.as_view({'post': 'refresh_token'}), name='refresh')
]
