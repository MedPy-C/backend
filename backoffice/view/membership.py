from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from backoffice.business_logic.membership import MembershipLogic
from backoffice.utils.validator import uuid_validator, slug_name_validator


class MembershipView(ViewSet):
    membership_logic = MembershipLogic()

    def list(self, request, user_login_code, slug_name):
        uuid_validator(user_login_code)
        slug_name_validator(slug_name)
        members_list = self.membership_logic.get_membership(user_login_code, slug_name)
        return Response(members_list, status=status.HTTP_200_OK)
