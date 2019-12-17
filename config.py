class BasicConfig:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class BasicSMTPConfig:
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = None
    MAIL_MAX_EMAILS = None
    MAIL_ASCII_ATTACHMENTS = False


class DevelopmentConfig(BasicConfig, BasicSMTPConfig):
    DEBUG = True
    PG_USER = 'temp_user'
    PG_PASSWORD = 'temp_password'
    PG_HOST = 'localhost'
    PG_PORT = 5432
    PG_DATABASE = 'test_bookshare'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{PG_USER}:{PG_PASSWORD}' \
                              f'@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'
    MAIL_USERNAME = 'test_username'
    MAIL_PASSWORD = 'test_password'

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
