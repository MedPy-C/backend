import uuid

from django.db import models

from backoffice.manager import group
from backoffice.models import UpdatedCreated, UserLogin


class Group(UpdatedCreated):
    group_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug_name = models.SlugField(max_length=40, unique=True)
    about = models.TextField()
    members = models.ManyToManyField(UserLogin, through="Membership", through_fields=('group', 'user'))
    is_verified = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    is_limited = models.BooleanField(default=True)
    members_limit = models.PositiveIntegerField(default=5)
    status = models.IntegerField()

    objects = group.GroupManager()
