from django.db import models, IntegrityError

from backoffice.utils.constant import Status
from backoffice.utils.exceptions import DuplicatedRecord, InvalidOperation


class MembershipQuerySet(models.QuerySet):

    def get_all(self, user_code):
        return self.filter(user=user_code, status=Status.ACTIVE.value)

    def get_by_membership_code(self, user_code, membership_code):
        return self.filter(user_login_code=user_code, membership_code=membership_code,
                           status=Status.ACTIVE.value).first()


class MembershipManager(models.Manager):
    def get_queryset(self):
        return MembershipQuerySet(self.model, using=self._db)

    def get_all_memberships(self, user_code):
        return self.get_queryset().get_all(user_code)

    def get_membership_by_membership_code(self, user_login_code, membership_code):
        return self.get_queryset().get_by_membership_code(user_login_code, membership_code)

    def save(self, membership):
        try:
            membership.save()
            return membership
        except IntegrityError:
            raise DuplicatedRecord()
        except Exception as ex:
            raise InvalidOperation(
                f"Error while trying to save membership \n Error Message:{ex}")

    def delete(self, membership):
        try:
            membership.status = Status.INACTIVE.value
            membership.save()
        except Exception as ex:
            raise InvalidOperation(f"Error while trying to delete membership, \n Error Message: {ex}")
