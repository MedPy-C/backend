import os

from .development import Development


# from .production import Production
# from .test import Test

def get_configs(enviroment=None):
    configs = {
        'dev': Development,
        # 'prd': Production,
        # 'test': Test
    }
    if not enviroment:
        enviroment = os.environ.get('MEDIAPP_BE_API_ENV', 'dev')
    return configs[enviroment]()


env = get_configs()
