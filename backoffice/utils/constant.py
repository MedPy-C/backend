from enum import Enum


class RoleLevel(Enum):
    OWNER = 0
    ADMIN = 1
    USER = 3


class Status(Enum):
    ACTIVE = 1
    INACTIVE = 0


class AccessLevel(Enum):
    ADMIN = 0
    USER = 1

class URL():
    ACTIVATION = '/backoffice/invitation/activate/'
