from django.db import models, IntegrityError

from backoffice.utils.constant import Status
from backoffice.utils.exceptions import DuplicatedRecord, InvalidOperation


class InvitationQuerySet(models.QuerySet):

    def get_all(self, user_code, slug_name):
        """
        get all the Invitation corresponding to the user_code
        :param slug_name: uuid
        :param user_code: uuid
        :return: a queryset with data of the Invitation that this user is part of.
        """
        return self.filter(issued_by=user_code, group__slug_name=slug_name, status=Status.ACTIVE.value)

    def get_by_invitation_code(self, invitation_code):
        """
        get a single Invitation for this particular user
        :param invitation_code: uuid
        :return: a python class of the Invitation model.
        """
        return self.filter(invitation_code=invitation_code, status=Status.ACTIVE.value).first()


class InvitationManager(models.Manager):
    def get_queryset(self):
        return InvitationQuerySet(self.model, using=self._db)

    def get_all_Invitations(self, user_code, slug_name):
        return self.get_queryset().get_all(user_code, slug_name)

    def get_invitation_by_code(self, invitation_code):
        return self.get_queryset().get_by_invitation_code(invitation_code)

    def save(self, invitation):
        try:
            invitation.save()
            return invitation
        except IntegrityError:
            raise DuplicatedRecord()
        except Exception as ex:
            raise InvalidOperation(
                f"Error while trying to save invitation \n Error Message:{ex}")

    def delete(self, invitation):
        try:
            invitation.status = Status.INACTIVE.value
            invitation.save()
        except Exception as ex:
            raise InvalidOperation(f"Error while trying to delete invitation, \n Error Message: {ex}")
