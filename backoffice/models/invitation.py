import uuid

from django.db import models

from backoffice.manager import invitation
from backoffice.models import UpdatedCreated, UserLogin, Group


class Invitation(UpdatedCreated):
    invitation_code = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    issued_by = models.ForeignKey(UserLogin, on_delete=models.CASCADE, related_name='issued_bye')
    used_by = models.ForeignKey(UserLogin, on_delete=models.CASCADE, blank=True, null=True, related_name='used_by')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.IntegerField()

    objecs = invitation.InvitationManager()
