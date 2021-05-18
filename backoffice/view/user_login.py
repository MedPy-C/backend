from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from backoffice.business_logic.user_login import UserLoginLogic
from backoffice.serializer.user_login import UserLoginAddSerializer
from backoffice.utils.validator import body_validator


class UserLoginView(ViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)
    user_login_logic = UserLoginLogic()
    def create(self, request):

        body_validator(request.data, UserLoginAddSerializer)
        self.user_login_logic.create(request.data)

        return Response(status=status.HTTP_201_CREATED)

    def list(self, request):
        user_login_list = self.user_login_logic.get_all()
        return Response(user_login_list, status.HTTP_200_OK)
