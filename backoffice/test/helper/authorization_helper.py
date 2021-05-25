from backoffice.business_logic.login import authenticate


def http_authorization_setup_by_current_user(username, password, client):
    staff_credential_data = authenticate(
        {'username': username, 'password': password})
    token = staff_credential_data.get('token')
    client.credentials(HTTP_AUTHORIZATION=token)

    return staff_credential_data.get('user_login_code')
