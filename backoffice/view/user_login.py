from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from backoffice.business_logic.user_login import UserLoginLogic
from backoffice.serializer.user_login import UserLoginAddSerializer
from backoffice.utils.decorators import access_level_required
from backoffice.utils.validator import body_validator


class UserLoginView(ViewSet):

    @access_level_required(min_access_level=AllowAny)
    def create(self, request):
        body_validator(request.data, UserLoginAddSerializer)

        UserLoginLogic().create(request.data)

        return Response(status=status.HTTP_201_CREATED)

    @access_level_required(min_access_level=AllowAny)
    def list(self, request):
        staff_list = UserLoginLogic().get_all()
        return Response(staff_list, status.HTTP_200_OK)
