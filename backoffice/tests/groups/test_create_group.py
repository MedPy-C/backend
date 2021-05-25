# from rest_framework import status
# from rest_framework.test import APITestCase
#
# from backoffice.business_logic.user_login import UserLoginLogic
# from backoffice.tests.helper.authorization_helper import http_authorization_setup_by_current_user
# from backoffice.tests.mock.group import group_payload
# from backoffice.tests.mock.user_login import owner_user_login
#
#
# class CreateGroupTest(APITestCase):
#
#     def setUp(self):
#         # seed a super staff
#         self.user_logic = UserLoginLogic()
#         self.user_logic.create(owner_user_login)
#         username = owner_user_login.get('username')
#         password = owner_user_login.get('password')
#
#         # set token to http authorization header
#         self.current_user_code = http_authorization_setup_by_current_user(
#             username, password, self.client)
#
#         self.url = f'/backoffice/user/{self.current_user_code}/group/'
#
#     def test_can_create_group(self):
#         new_group = group_payload.copy()
#         response = self.client.post(
#             self.url, new_group, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
