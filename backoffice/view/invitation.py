from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from backoffice.business_logic.invitation import InvitationLogic
from backoffice.utils.validator import uuid_validator, slug_name_validator


class InvitationView(ViewSet):
    invitation_logic = InvitationLogic()

    def create(self, request, user_login_code, slug_name):
        uuid_validator(user_login_code)
        slug_name_validator(slug_name)
        created_invitation = self.invitation_logic.create(user_login_code, slug_name)
        return Response(created_invitation, status=status.HTTP_201_CREATED)

    def list(self, request, user_login_code, slug_name):
        uuid_validator(user_login_code)
        slug_name_validator(slug_name)
        invitation_list = self.invitation_logic.list(user_login_code, slug_name)
        return Response(invitation_list, status=status.HTTP_200_OK)

    def activate(self, request, invitation_code):
        uuid_validator(invitation_code)
        new_member = self.invitation_logic.activate(invitation_code, request)
        return Response(new_member, status=status.HTTP_200_OK)