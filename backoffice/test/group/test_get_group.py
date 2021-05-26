import uuid

from rest_framework import status
from rest_framework.test import APITestCase

from backoffice.business_logic.user_login import UserLoginLogic
from backoffice.test.helper.authorization_helper import http_authorization_setup_by_current_user
from backoffice.test.mock.group import group_payload
from backoffice.test.mock.user_login import owner_user_login
from backoffice.test.seeders.group import seed_group


class GetGroupTest(APITestCase):

    def setUp(self):
        # seed a super staff
        self.user_logic = UserLoginLogic()
        self.user_logic.create(owner_user_login)
        username = owner_user_login.get('username')
        password = owner_user_login.get('password')

        # set token to http authorization header
        self.current_user_code = http_authorization_setup_by_current_user(
            username, password, self.client)
        #seed group
        current_group = seed_group(
            self.current_user_code, group_payload.copy())
        self.group_code = str(current_group['group_code'])
        self.url_without_group_code = f'/backoffice/user/{self.current_user_code}/group/'
        self.url = f'/backoffice/user/{self.current_user_code}/group/{self.group_code}'

    def test_can_get_group(self):
        response = self.client.get(
            self.url_without_group_code, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_existing_group(self):
        non_existing_group_code = str(uuid.uuid4())
        url = self.url_without_group_code+non_existing_group_code+'/'
        response = self.client.get(
            url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_group_with_non_user_code(self):
        user_code = ' '
        url = f'/backoffice/user/{user_code}/group/{self.group_code}/'
        response = self.client.get(
            url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
