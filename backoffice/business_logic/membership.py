from django.forms import model_to_dict

from backoffice import models
from backoffice.utils.constant import RoleLevel
from backoffice.utils.exceptions import EntityNotFound


class MembershipLogic():

    def __init__(self):
        self.fields = []

    def get_membership(self, user_login_code, slug_name):
        user = models.UserLogin.objects.get_user_by_code(user_login_code)
        if not user:
            raise EntityNotFound(
                f'User with code {user_login_code} not found.'
            )
        group = models.Group.objects.get_group_by_group_slug_name(user_login_code, slug_name)
        if not group:
            raise EntityNotFound(
                f'Group with code {slug_name} not found.'
            )
        members = models.Membership.objects.get_all_members_by_slug_name(slug_name)
        members_list = []
        if not members:
            return []
        for member in members:
            members_list.append(self.__mapped_members(member))
        return members_list

    def __mapped_members(self, membership):
        members_dict = model_to_dict(membership, fields=self.fields)
        members_dict['username'] = str(membership.user.username)
        members_dict['name'] = str(membership.user.name)
        members_dict['invited_by'] = '' if not membership.invited_by else str(membership.invited_by.name)
        members_dict['role'] = str(RoleLevel(membership.role))
        return members_dict
