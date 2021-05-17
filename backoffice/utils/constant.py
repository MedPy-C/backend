from enum import Enum


class AccessLevel(Enum):
    ADMIN = 0
    USER = 1

class Status(Enum):
    ACTIVE = 1
    INACTIVE = 0
