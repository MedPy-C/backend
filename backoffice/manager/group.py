from django.db import models, IntegrityError

from backoffice.utils.constant import Status
from backoffice.utils.exceptions import DuplicatedRecord, InvalidOperation


class GroupQuerySet(models.QuerySet):

    def get_all(self, user_code):
        """
        get all the groups corresponding to the user_code
        :param user_code: uuid
        :return: a queryset with data of the groups that this user is part of.
        """
        return self.filter(membership__user=user_code, status=Status.ACTIVE.value)

    def get_by_group_slug_name(self, user_code, slug_name):
        """
        get a single groups for this particular user
        :param user_code: uuid
        :param slug_name: slug name of the groups
        :return: a python class of the groups model.
        """
        return self.filter(membership__user=user_code, membership__group__slug_name=slug_name,
                           status=Status.ACTIVE.value).first()

    def get_by_group_code(self, group_code):
        return self.filter(group_code=group_code, status=Status.ACTIVE.value).first()


class GroupManager(models.Manager):
    def get_queryset(self):
        return GroupQuerySet(self.model, using=self._db)

    def get_all_groups(self, user_code):
        return self.get_queryset().get_all(user_code)

    def get_group_by_group_slug_name(self, user_login_code, slug_name):
        return self.get_queryset().get_by_group_slug_name(user_login_code, slug_name)

    def get_group_by_group_code(self, group_code):
        return self.get_queryset().get_by_group_code(group_code)

    def save(self, group):
        try:
            group.save()
            return group
        except IntegrityError:
            raise DuplicatedRecord()
        except Exception as ex:
            raise InvalidOperation(
                f"Error while trying to save groups \n Error Message:{ex}")

    def delete(self, group):
        try:
            group.status = Status.INACTIVE.value
            group.save()
        except Exception as ex:
            raise InvalidOperation(f"Error while trying to delete groups, \n Error Message: {ex}")
