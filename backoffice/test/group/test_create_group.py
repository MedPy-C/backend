import uuid

from rest_framework import status
from rest_framework.test import APITestCase

from backoffice.business_logic.user_login import UserLoginLogic
from backoffice.test.helper.authorization_helper import http_authorization_setup_by_current_user
from backoffice.test.mock.group import group_payload
from backoffice.test.mock.user_login import owner_user_login


class CreateGroupTest(APITestCase):

    def setUp(self):
        # seed a super staff
        self.user_logic = UserLoginLogic()
        self.user_logic.create(owner_user_login)
        username = owner_user_login.get('username')
        password = owner_user_login.get('password')

        # set token to http authorization header
        self.current_user_code = http_authorization_setup_by_current_user(
            username, password, self.client)

        self.url = f'/backoffice/user/{self.current_user_code}/group/'

    def test_can_create_group(self):
        new_group = group_payload.copy()
        response = self.client.post(
            self.url, new_group, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_group_without_body(self):
        response = self.client.post(
            self.url, None, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_group_without_name(self):
        new_group_without_name = group_payload.copy()
        new_group_without_name['name'] = ''
        response = self.client.post(
            self.url, new_group_without_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_group_without_slug_name(self):
        new_group_without_slug_name = group_payload.copy()
        new_group_without_slug_name['slug_name'] = ''
        response = self.client.post(
            self.url, new_group_without_slug_name, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_group_without_about(self):
        new_group_without_about = group_payload.copy()
        new_group_without_about['about'] = ''
        response = self.client.post(
            self.url, new_group_without_about, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_group_non_existing_user(self):
        new_group = group_payload.copy()
        current_user_code = str(uuid.uuid4())
        url = f'/backoffice/user/{current_user_code}/group/'
        response = self.client.post(
            url, new_group, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
