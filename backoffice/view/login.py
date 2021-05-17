from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from backoffice.business_logic import login
from backoffice.utils.validator import body_validator
from backoffice.serializer.login import LoginSerializer, LoginRefreshSerializer


class Login(viewsets.ViewSet):
    serializer_class = LoginSerializer

    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)
    login_logic = login

    def authenticate(self, request):
        login = body_validator(request.data, LoginSerializer)
        user_login = self.login_logic.authenticate(login)
        return Response(user_login)

    def refresh_token(self, request):
        payload = body_validator(request.data, LoginRefreshSerializer)
        refresh_token = self.login_logic.refresh_token(payload)
        return Response(refresh_token)