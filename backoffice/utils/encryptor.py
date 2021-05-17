import hashlib


class Encryptor:
    @staticmethod
    def md5_encryption(raw_value):
        return hashlib.md5(raw_value.encode('utf-8')).hexdigest()
