from functools import wraps
from .exceptions import StaffNotAllowed

def access_level_required(min_access_level):
    def decorator_access_level(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            token_user = request.user
            if token_user.get('access_level') < min_access_level:
                raise StaffNotAllowed('Staff is not allowed to create a new Staff')
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator_access_level