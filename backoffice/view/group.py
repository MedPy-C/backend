from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from backoffice.business_logic.group import GroupLogic
from backoffice.serializer.group import GroupSerializer
from backoffice.utils.validator import body_validator, uuid_validator


class GroupView(ViewSet):
    group_logic = GroupLogic()

    def update(self):
        pass

    def create(self, request, user_login_code):
        uuid_validator(user_login_code)
        body_validator(request.data, GroupSerializer)
        self.group_logic.create(user_login_code, request.data)
        return Response(status=status.HTTP_201_CREATED)

    def retrieve(self):
        pass

    def delete(self):
        pass

    def list(self, request, user_login_code):
        uuid_validator(user_login_code)
        group_list = self.group_logic.list(user_login_code)
        return Response(group_list, status=status.HTTP_200_OK)
