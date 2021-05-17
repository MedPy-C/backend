import datetime

import jwt

from backoffice.models.user_login import UserLogin
from backoffice.utils.encryptor import Encryptor
from mediapp_be.settings import SECRET_KEY


def authenticate(login_payload):
    username = login_payload.get('username').lower()
    password = login_payload.get('password')
    password_encrypted = Encryptor.md5_encryption(password)

    try:
        user_login = UserLogin.objects.authenticate(username, password_encrypted)
        user_login_code = str(user_login.user_login_code)
        name = user_login.name

        status = user_login.status
        access_level = user_login.access_level
        token = __generate_jwt_token(access_level, user_login_code, name, status)

        return {
            'token': token,
            'user_login_code': user_login_code,
            'name': name,
            'access_level': access_level,
        }
    except Exception as error:
        raise error


def refresh_token(payload):
    token = payload.get('old_token')
    user_login_code = payload.get('user_login_code')

    try:
        old_token_payload = jwt.decode(
            token, SECRET_KEY, algorithm='HS256'
        )
        if old_token_payload.get('user_login_code') == user_login_code:
            old_token_values = old_token_payload.values()
            refresh_token = __generate_jwt_token(*old_token_values)
            return {
                'token': refresh_token
            }
        raise Exception('Invalid Token')

    except jwt.ExpiredSignature:
        raise Exception('Token expired, make the login again')


def __generate_jwt_token(access_level, user_login_code, name, status, now=None, *args, expiration_days=3):
    if not now:
        now = datetime.datetime.utcnow()
    expiration = datetime.datetime.utcnow() + datetime.timedelta(days=expiration_days)

    token_payload = {
        'access_level': access_level,
        'user_login_code': user_login_code,
        'name': name,
        'status': status,
        'iat': now,
        'exp': expiration,
    }
    token = jwt.encode(token_payload,
                       SECRET_KEY,
                       algorithm='HS256').decode('utf-8')
    return f"Bearer {token}"