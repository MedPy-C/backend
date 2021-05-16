class Test:

    def __init__(self):
        self.db = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
        self.allowed_hosts = [
            '127.0.0.1', 'localhost'
        ]
        self.debug = False
