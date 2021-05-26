from django.db import models, IntegrityError

from backoffice.utils.constant import Status
from backoffice.utils.exceptions import DuplicatedRecord, InvalidOperation


class MembershipQuerySet(models.QuerySet):

    def get_all(self, user_code):
        return self.filter(user=user_code, status=Status.ACTIVE.value)

    def get_by_membership_code(self, user_code, membership_code):
        return self.filter(user_login_code=user_code, membership_code=membership_code,
                           status=Status.ACTIVE.value).first()

    def get_role_by_user_code_slug_name(self, user_code, slug_name):
        return self.filter(user=user_code, group__slug_name=slug_name, status=Status.ACTIVE.value).values('role')

    def get_membership_data(self, user_code, slug_name):
        return self.filter(user=user_code, group__slug_name=slug_name, status=Status.ACTIVE.value).first()

    def get_membership_by_user_code_group_code(self, user_code, group_code):
        return self.filter(user=user_code, group=group_code).first()

    def get_membership_count(self, slug_name):
        return self.filter(group__slug_name=slug_name).count()

    def get_all_members(self, slug_name):
        return self.filter(group__slug_name=slug_name, status=Status.ACTIVE.value)


class MembershipManager(models.Manager):
    def get_queryset(self):
        return MembershipQuerySet(self.model, using=self._db)

    def get_all_memberships(self, user_code):
        return self.get_queryset().get_all(user_code)

    def get_membership_data_by_user_code_slug_name(self, user_code, slug_name):
        return self.get_queryset().get_membership_data(user_code, slug_name)

    def get_membership_by_membership_code(self, user_login_code, membership_code):
        return self.get_queryset().get_by_membership_code(user_login_code, membership_code)

    def get_member_role_by_user_code_group_slug_name(self, user_login_code, slug_name):
        return self.get_queryset().get_role_by_user_code_slug_name(user_login_code, slug_name)

    def get_membership_count_by_group_slug_name(self, slug_name):
        return self.get_queryset().get_membership_count(slug_name)

    def get_membership_by_user_code_group_code(self, user_code, group_code):
        return self.get_queryset().get_membership_by_user_code_group_code(user_code, group_code)

    def get_all_members_by_slug_name(self, slug_name):
        return self.get_queryset().get_all_members(slug_name)

    def save(self, membership):
        try:
            membership.save()
            return membership
        except IntegrityError as ex:
            raise DuplicatedRecord({ex})
        except Exception as ex:
            raise InvalidOperation(
                f"Error while trying to save membership \n Error Message:{ex}")

    def delete(self, membership):
        try:
            membership.status = Status.INACTIVE.value
            membership.save()
        except Exception as ex:
            raise InvalidOperation(f"Error while trying to delete membership, \n Error Message: {ex}")
