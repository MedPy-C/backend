from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from backoffice.business_logic import login
from backoffice.utils.validator import body_validator
from backoffice.serializer.login import LoginSerializer, LoginRefreshSerializer


class LoginViewSet(ViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)
    login_logic = login

    def authenticate(self, request):
        login = body_validator(request.data, LoginSerializer)
        username = self.login_logic.authenticate(login)
        return Response(username)

    def refresh_token(self, request):
        payload = body_validator(request.data, LoginRefreshSerializer)
        refresh_token = self.login_logic.refresh_token(payload)
        return Response(refresh_token)
