import uuid

from django.db import models
from backoffice.manager import users_login
from backoffice.models import UpdatedCreated


class UserLogin(UpdatedCreated):
    user_login_code = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user_login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    access_level = models.IntegerField()
    email = models.CharField(max_length=250, unique=True)
    phone_number = models.CharField(max_length=18, unique=True)
    status = models.IntegerField()

    objects = users_login.UserLoginManager()
