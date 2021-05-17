from django.db import models
from django.db import IntegrityError

from backoffice.utils.constant import Status
from backoffice.utils.exceptions import EntityNotFound, DuplicatedRecord, InvalidOperation


class UserLoginQuerySet(models.QuerySet):
    def authenticate(self, user_login, password):
        return self.get(user_login=user_login, password=password, status=Status.ACTIVE.value)

    def get_all(self):
        return self.filter(status=Status.ACTIVE.value).values('user_login_code', 'user_login', 'name', 'email', 'access_level')

    def get_by_code(self, code):
        return self.filter(user_login_code=code, status=Status.ACTIVE.value).first()


class UserLoginManager(models.Manager):
    def get_queryset(self):
        return UserLoginQuerySet(self.model, using=self._db)

    def authenticate(self, user_login, password):
        try:
            return self.get_queryset().authenticate(user_login, password)
        except models.ObjectDoesNotExist:
            raise EntityNotFound('UserLogin member was not found')

    def users_login(self):
        return self.get_queryset().get_all()

    def user_login_by_code(self, code):
        return self.get_queryset().get_by_code(code)

    def save(self, user_login):
        try:
            user_login.save()
            return user_login
        except IntegrityError:
            raise DuplicatedRecord()
        except Exception as ex:
            raise InvalidOperation(
                f"Error while trying to save user \n Error Message:{ex}")