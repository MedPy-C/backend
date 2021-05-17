from django.urls import path, include
from rest_framework.routers import SimpleRouter

from backoffice.view import user_login

user_login_router = SimpleRouter()
user_login_router.register(
    prefix=r'user-login', viewset=user_login.UserLoginView, basename="users-login")

staff_routes = [
    path('', include(user_login_router.urls))
]
