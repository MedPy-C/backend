from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from backoffice.business_logic.group import GroupLogic
from backoffice.serializer.group import GroupSerializer
from backoffice.utils.decorators import check_ownership
from backoffice.utils.validator import body_validator, uuid_validator, slug_name_validator


class GroupView(ViewSet):
    group_logic = GroupLogic()

    @check_ownership()
    def update(self, request, user_login_code, slug_name):
        uuid_validator(user_login_code)
        slug_name_validator(slug_name)
        body_validator(request.data, GroupSerializer)
        updated_group = self.group_logic.update(user_login_code, slug_name, request.data)
        return Response(updated_group, status=status.HTTP_200_OK)

    @check_ownership()
    def create(self, request, user_login_code):
        uuid_validator(user_login_code)
        body_validator(request.data, GroupSerializer)
        self.group_logic.create(request, user_login_code, request.data)
        return Response(status=status.HTTP_201_CREATED)

    @check_ownership()
    def retrieve(self, request, user_login_code, slug_name):
        uuid_validator(user_login_code)
        slug_name_validator(slug_name)
        group = self.group_logic.retrieve(request, user_login_code, slug_name)
        return Response(group, status=status.HTTP_200_OK)

    @check_ownership()
    def delete(self, request, user_login_code, slug_name):
        uuid_validator(user_login_code)
        slug_name_validator(slug_name)
        self.group_logic.delete(request, user_login_code, slug_name)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @check_ownership()
    def list(self, request, user_login_code):
        uuid_validator(user_login_code)
        group_list = self.group_logic.list(request, user_login_code)
        return Response(group_list, status=status.HTTP_200_OK)
