from django.db import models, IntegrityError

from backoffice.utils.constant import Status
from backoffice.utils.exceptions import DuplicatedRecord, InvalidOperation


class GroupQuerySet(models.QuerySet):

    def get_all(self, user_code):
        return self.filter(user_login_code=user_code, status=Status.ACTIVE.value)

    def get_by_group_code(self, user_code, group_code):
        return self.filter(user_login_code=user_code, group_code=group_code, status=Status.ACTIVE.value).first()


class GroupManager(models.Manager):
    def get_queryset(self):
        return GroupQuerySet(self.model, using=self._db)

    def get_all_groups(self, user_code):
        return self.get_queryset().get_all(user_code)

    def get_group_by_group_code(self, user_login_code, group_code):
        return self.get_queryset().get_by_group_code(user_login_code, group_code)

    def save(self, group):
        try:
            group.save()
            return group
        except IntegrityError:
            raise DuplicatedRecord()
        except Exception as ex:
            raise InvalidOperation(
                f"Error while trying to save user \n Error Message:{ex}")

    def delete(self, group):
        try:
            group.status = Status.INACTIVE.value
            group.save()
        except Exception as ex:
            raise InvalidOperation(f"Error while trying to delete user, \n Error Message: {ex}")
