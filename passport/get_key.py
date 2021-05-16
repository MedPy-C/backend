def get_secret_key(BASE_DIR):
    key = ''
    with open(f'{BASE_DIR}/passport/private_key.pem') as secret_file:
        key = secret_file.read().replace('\n', '').replace(
            '-', '').replace('BEGIN RSA PRIVATE KEY', '').replace('END RSA PRIVATE KEY', '')
    return key