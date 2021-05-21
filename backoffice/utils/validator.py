import re
import uuid

from backoffice.utils.constant import AccessLevel
from backoffice.utils.exceptions import InvalidParameter


def body_validator(data, serializer):
    body_serialized = serializer(data=data)
    if not body_serialized.is_valid():
        message = body_serialized.errors
        raise InvalidParameter(message)
    return body_serialized.data


def password_validator(password):
    if not password:
        raise InvalidParameter('password is required.')
    elif len(password) < 6:
        raise InvalidParameter(
            "invalid password: password must contain at least 6 characters.")
    else:
        regEx = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]"
        pattern = re.compile(regEx)
        match = re.search(pattern, password)
        if not match:
            raise InvalidParameter(
                "invalid password: password must contain at least 1 uppercase, 1 lowercase, 1 number and 1 special character.")
    return password


def access_level_validator(access_level):
    if access_level:
        try:
            return AccessLevel(access_level).value
        except Exception:
            raise InvalidParameter(
                "access_level is invalid.")
    return access_level

def uuid_validator(uuid_code):
    try:
        uuid.UUID(uuid_code)
    except ValueError:
        raise InvalidParameter(
            "uuid is invalid.")
