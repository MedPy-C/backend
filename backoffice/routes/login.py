from django.urls import path

from backoffice.business_logic import login

login_routes = [
    path('login/', login.Login.as_view({'post': 'authenticate'}), name='authentication'),
    path('login/refresh/', login.Login.as_view({'post': 'refresh_token'}), name='refresh')
]
