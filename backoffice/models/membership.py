import uuid

from django.db import models
from backoffice.manager import membership
from backoffice.models import UpdatedCreated, UserLogin, Group


class Membership(UpdatedCreated):
    membership_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserLogin, on_delete=models.CASCADE, blank=True, null=True, db_column='membership_user')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, db_column='membership_group')
    role = models.IntegerField()
    status = models.IntegerField()
    used_invitations = models.PositiveIntegerField(default=0)
    remaining_invitations = models.PositiveIntegerField(default=5)
    invited_by = models.ForeignKey("UserLogin", blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='invited_by')

    objects = membership.MembershipManager()
