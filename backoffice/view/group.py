from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from backoffice.business_logic.group import GroupLogic
from backoffice.serializer.group import GroupSerializer
from backoffice.utils.validator import body_validator, uuid_validator, slug_name_validator


class GroupView(ViewSet):
    group_logic = GroupLogic()

    def update(self, request, user_login_code, slug_name):
        uuid_validator(user_login_code)
        slug_name_validator(slug_name)
        body_validator(request.data, GroupSerializer)
        updated_group = self.group_logic.update(user_login_code, slug_name, request.data)
        return Response(updated_group, status=status.HTTP_200_OK)

    def create(self, request, user_login_code):
        uuid_validator(user_login_code)
        body_validator(request.data, GroupSerializer)
        self.group_logic.create(user_login_code, request.data)
        return Response(status=status.HTTP_201_CREATED)

    def retrieve(self, request, user_login_code, slug_name):
        uuid_validator(user_login_code)
        slug_name_validator(slug_name)
        group = self.group_logic.retrieve(user_login_code, slug_name)
        return Response(group, status=status.HTTP_200_OK)

    def delete(self, request, user_login_code, group_code):
        uuid_validator(user_login_code)
        uuid_validator(group_code)
        self.group_logic.delete(user_login_code, group_code)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, user_login_code):
        uuid_validator(user_login_code)
        group_list = self.group_logic.list(user_login_code)
        return Response(group_list, status=status.HTTP_200_OK)
