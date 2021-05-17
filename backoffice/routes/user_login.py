from django.urls import path, include
from rest_framework.routers import SimpleRouter

from backoffice.view import user_login

staff_router = SimpleRouter()
staff_router.register(
    prefix=r'user-login', viewset=user_login.UserLoginView, basename="users-login")

staff_routes = [
    path('', include(staff_router.urls))
]