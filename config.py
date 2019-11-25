class BasicConfig:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True


class DevelopmentConfig(BasicConfig):
    DEBUG = True
    PG_USER = 'temp_user'
    PG_PASSWORD = 'temp_password'
    PG_HOST = 'localhost'
    PG_PORT = 5432
    PG_DATABASE = 'test_bookshare'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{PG_USER}:{PG_PASSWORD}' \
                              f'@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'


class TestingConfig(DevelopmentConfig):
    TESTING = True


class ProductionConfig(BasicConfig):
    """Should be implemented in production environment"""


CONFIG_MAP = {'test': TestingConfig,
              'prod': ProductionConfig,
              'dev': DevelopmentConfig}


def get_config(env):

    if not isinstance(env, str):
        raise ValueError('Name of configuration object should be a string')

    return CONFIG_MAP.get(env, BasicConfig)
