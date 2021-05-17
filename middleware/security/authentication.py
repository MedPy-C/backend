import jwt
from rest_framework.authentication import BaseAuthentication

from backoffice.utils import exceptions
from mediapp_be import settings


class Mediapp_beAuthentication(BaseAuthentication):

    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header or 'Bearer' not in authorization_header:
            raise exceptions.InvalidToken()

        try:
            access_token = authorization_header.replace('Bearer ', '')
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            return (payload, None)
        except jwt.ExpiredSignatureError:
            raise exceptions.TokenExpired()
        except (jwt.InvalidSignatureError, jwt.DecodeError):
            raise exceptions.InvalidToken()
