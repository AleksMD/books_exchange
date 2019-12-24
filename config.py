import os
import dotenv


env_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(env_path)


class BasicConfig:
    HOST = '0.0.0.0'
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
    PG_USER = os.getenv('PG_USER')
    PG_PASSWORD = os.getenv('PG_PASSWORD')
    PG_HOST = os.getenv('PG_HOST')
    PG_PORT = os.getenv('PG_PORT')
    PG_DATABASE = os.getenv('PG_DATABASE')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{PG_USER}:{PG_PASSWORD}' \
                              f'@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_SUPPRESS_SEND = True


class TestingConfig(DevelopmentConfig):
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = True


class ProductionConfig(BasicConfig):
    """Should be implemented in production environment"""


CONFIG_MAP = {'test': TestingConfig,
              'prod': ProductionConfig,
              'dev': DevelopmentConfig}


def get_config(env):

    if not isinstance(env, str):
        raise ValueError('Name of configuration object must be a string')

    return CONFIG_MAP.get(env, BasicConfig)
