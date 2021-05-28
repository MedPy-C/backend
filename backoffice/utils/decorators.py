from functools import wraps
from .exceptions import IsNotOwner


def check_ownership():
    def decorator_check_ownership(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            user_login_code = str(request.user.get('user_login_code'))
            user_login_code_url = str(kwargs.get('user_login_code'))
            if user_login_code != user_login_code_url:
                raise IsNotOwner(
                    'The user does not have the permissions')
            return func(self, request, *args, **kwargs)

        return wrapper

    return decorator_check_ownership
