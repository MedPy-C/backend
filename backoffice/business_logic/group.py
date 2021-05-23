from django.forms import model_to_dict

from backoffice import models
from backoffice.utils.constant import Status, RoleLevel
from backoffice.utils.exceptions import EntityNotFound, UnAuthorized


class GroupLogic():
    """
    Group business logic.
    Methods:
        create(): create a new group
        list(): list all of groups that the user it's part of.
        retrieve(): get a data from a single group
        update(): update the group
        delete(): perform a soft delete
    """

    def __init__(self):
        self.fields = ['name', 'slug_name', 'about']

    def create(self, user_login_code, group_data):
        """
        create function of group model
        :param user_login_code: uuid
        :param group_data: serialized data of group
        :return: if no errors present does not raise exceptions.
        """
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
        """
        list user group by user code
        :param user_login_code: uuid
        :return: a list of dict with data of the group that the user it is part of.
        """
        user = models.UserLogin.objects.get_user_by_code(user_login_code)
        if not user:
            raise EntityNotFound(
                f'User with code {user_login_code} not found.'
            )
        groups = models.Group.objects.get_all_groups(user_login_code)
        group_list = []
        for group in groups:
            group_list.append(self.__mapped_group(group))
        return group_list

    def retrieve(self, user_login_code, slug_name):
        """
        retrive only one group,
        :param user_login_code: uuid
        :param slug_name: slug name of the group
        :return: a dict with data of the selected group.
        """
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
        return self.__mapped_group_detailed(group)

    def update(self, login_user_code, slug_name, group_data):
        user = models.UserLogin.objects.get_user_by_code(login_user_code)
        if not user:
            raise EntityNotFound(
                f'User with code {login_user_code} not found'
            )
        group = models.Group.objects.get_group_by_group_slug_name(login_user_code, slug_name)
        if not group:
            raise EntityNotFound(
                f'Group with code {slug_name} not found.'
            )
        role = models.Membership.objects.get_member_role_by_user_code_group_code(login_user_code, group_code)
        for x in role:
            print(x['role'])
            if x['role'] != RoleLevel.OWNER.value:
                raise UnAuthorized(
                    f'User with code {login_user_code} does not have the privileges to perform that action.'
                )
        group.name = group_data.get('name')
        group.slug_name = group_data.get('slug_name')
        group.about = group_data.get('about')
        # if is_owner
        group_saved = models.Group.objects.save(group)
        return self.__mapped_group(group_saved)

    def delete(self, login_user_code, group_code):
        user = models.UserLogin.objects.get_user_by_code(login_user_code)
        if not user:
            raise EntityNotFound(
                f'User with code {login_user_code} not found'
            )
        group = models.Group.objects.get_group_by_group_code(login_user_code, group_code)
        if not group:
            raise EntityNotFound(
                f'Group with code {group_code} not found.'
            )
        role = models.Membership.objects.get_member_role_by_user_code_group_code(login_user_code, group_code)
        for x in role:
            print(x['role'])
            if x['role'] != RoleLevel.OWNER.value:
                raise UnAuthorized(
                    f'User with code {login_user_code} does not have the privileges to perform that action.'
                )
        models.Group.objects.delete(group)

    def __mapped_group_detailed(self, group):
        """
        we map from group object to a dict with data of group
        :param group: python class object
        :return: dict with more detailed data of group.
        """
        group_dict = model_to_dict(group, fields=self.fields)
        group_dict['group_code'] = str(group.group_code)
        group_dict['created_at'] = str(group.created_at)
        group_dict['is_verified'] = str(group.is_verified)
        group_dict['is_public'] = str(group.is_public)
        return group_dict

    def __mapped_group(self, group):
        """
        we map from group object to a dict with data of group
        :param group: python class object
        :return: dict with data of group.
        """
        group_dict = model_to_dict(group, fields=self.fields)
        group_dict['group_code'] = str(group.group_code)
        return group_dict
