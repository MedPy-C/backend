from django.forms import model_to_dict

from backoffice import models
from backoffice.utils.constant import Status, RoleLevel
from backoffice.utils.exceptions import EntityNotFound


class GroupLogic():
    def __init__(self):
        self.fields = ['membership_code', 'group']

    def create(self, user_login_code, group_data):
        user = models.UserLogin.objects.get_user_by_code(user_login_code)
        if not user:
            raise EntityNotFound(
                f'User with code {user_login_code} not found'
            )
        group_model = models.Group()
        membership_model = models.Membership()

        group_model.name = group_data.get('name')
        group_model.slug_name = group_data.get('slug_name')
        group_model.about = group_data.get('about')
        group_model.status = Status.ACTIVE.value
        saved_group = models.Group.objects.save(group_model)

        membership_model.group = saved_group
        membership_model.status = Status.ACTIVE.value
        membership_model.role = RoleLevel.OWNER.value
        membership_model.user = user
        saved_membership = models.Membership.objects.save(membership_model)

    def list(self, user_login_code):
        user = models.UserLogin.objects.get_user_by_code(user_login_code)
        if not user:
            raise EntityNotFound(
                f'User with code {user_login_code} not found.'
            )
        # groups = models.Group.objects.get_all_groups(user_login_code)
        groups = models.Membership.objects.get_all_memberships(user_login_code)
        group_list = []
        for group in groups:
            group_list.append(self.__mapped_group(group))
        return group_list

    def __mapped_group(self, membership):
        group_dict = model_to_dict(membership, fields=self.fields)
        group_dict['membership_code'] = str(membership.membership_code)
        return group_dict
