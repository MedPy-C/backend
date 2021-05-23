class ErrorCode:
    INVALID_PARAMETER = 0
    INVALID_TOKEN = 1
    UNAUTHORIZED = 2
    NOT_FOUND = 3
    UNEXPECTED = 4
    DUPLICATED = 5


class InvalidParameter(Exception):
    def __init__(self, message='Invalid Parameter'):
        self.error_code = ErrorCode.INVALID_PARAMETER
        self.status_code = 400
        self.message = message
        super().__init__(self.message)


class InvalidToken(Exception):
    def __init__(self, message='Invalid token format'):
        self.error_code = ErrorCode.INVALID_TOKEN
        self.status_code = 401
        self.message = message
        super().__init__(self.message)


class TokenExpired(Exception):
    def __init__(self, message='Token is expired'):
        self.error_code = ErrorCode.UNAUTHORIZED
        self.status_code = 401
        self.message = message
        super().__init__(self.message)


class StaffNotAllowed(Exception):
    def __init__(self, message='Staff is not allowed'):
        self.error_code = ErrorCode.UNAUTHORIZED
        self.status_code = 403
        self.message = message
        super().__init__(self.message)


class EntityNotFound(Exception):
    def __init__(self, message='Entity not found'):
        self.error_code = ErrorCode.NOT_FOUND
        self.status_code = 404
        self.message = message
        super().__init__(self.message)


class InvalidOperation(Exception):
    def __init__(self, message='Invalid operation exception'):
        self.error_code = ErrorCode.UNEXPECTED
        self.status_code = 500
        self.message = message
        super().__init__(self.message)


class DuplicatedRecord(Exception):
    def __init__(self, message='Duplicate record does not allow'):
        self.error_code = ErrorCode.DUPLICATED
        self.status_code = 409
        self.message = message
        super().__init__(self.message)

class UnAuthorized(Exception):
    def __init__(self, message='UnAuthorized'):
        self.error_code = ErrorCode.UNAUTHORIZED
        self.status_code = 402
        self.message = message
        super().__init__(self.message)
