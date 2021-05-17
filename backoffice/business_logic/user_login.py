from backoffice import models
from backoffice.utils.constant import AccessLevel, Status
from backoffice.utils.encryptor import Encryptor


class UserLoginLogic():

    def __init__(self):
        self.fields = ['name', 'access_level', 'email', 'phone_number']


    def create(self, staff_data):
        user_login = staff_data.get('staff_login').lower()
        email = staff_data.get('email').lower()
        password = staff_data.get('password')
        password_encrypted = Encryptor.md5_encryption(password)
        name = staff_data.get('name')
        phone_number = staff_data.get('phone_number')

        access_level = staff_data.get('access_level')
        if not access_level:
            access_level = AccessLevel.USER.value

        new_user_login = models.UserLogin(user_login=user_login,
                             name=name,
                             password=password_encrypted,
                             email=email,
                             phone_number=phone_number,
                             access_level=access_level,
                             status=Status.ACTIVE.value
                             )

        user_login_saved = models.UserLogin.objects.save(new_user_login)

        return user_login_saved