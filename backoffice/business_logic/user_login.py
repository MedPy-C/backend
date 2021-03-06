from backoffice import models
from backoffice.utils.constant import AccessLevel, Status
from backoffice.utils.encryptor import Encryptor


class UserLoginLogic():

    def __init__(self):
        self.fields = ['name', 'email', 'phone_number']

    def create(self, user_login_data):
        username = user_login_data.get('username').lower()
        email = user_login_data.get('email').lower()
        password = user_login_data.get('password')
        password_encrypted = Encryptor.md5_encryption(password)
        name = user_login_data.get('name')
        phone_number = user_login_data.get('phone_number')
        new_user_login = models.UserLogin(username=username,
                                          name=name,
                                          password=password_encrypted,
                                          email=email,
                                          phone_number=phone_number,
                                          status=Status.ACTIVE.value
                                          )

        user_login_saved = models.UserLogin.objects.save(new_user_login)

        return user_login_saved

    def get_all(self):
        user_login_list = models.UserLogin.objects.get_all_users()

        for user_login in user_login_list:
            user_login['user_login_code'] = str(user_login['user_login_code'])

        return user_login_list
