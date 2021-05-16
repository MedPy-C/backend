# from pathlib import Path
from pathlib import Path


class Development:
    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parent.parent
        self.db = {
            # 'ENGINE': 'django.db.backends.postgresql',
            # 'NAME': 'postgres',
            # 'USER': 'postgres',
            # 'PASSWORD': 'postgres',
            # 'HOST': 'postgres_database',
            # 'PORT': 5432
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            # 'NAME': ':memory:'
        }
        self.allowed_hosts = [
            '127.0.0.1', 'localhost'
        ]
        self.debug = True
