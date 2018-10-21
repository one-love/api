import os

SECRET_KEY = 'iQfPvB6sZaNHqVFI5CJa9rM1xOEVHKIM0LwifT04yLsPlZhSSvaDuZXOgJFSpJVq'
REDIS_HOST = 'redis'


class Config:
    DEBUG = False
    SECURITY_PASSWORD_SALT = 'tilda'
    SECRET_KEY = SECRET_KEY
    SECURITY_TRACKABLE = False
    JWT_SECRET_KEY = SECRET_KEY
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_PATH = '/api/v0'
    JWT_REFRESH_COOKIE_PATH = '/api/v0/auth/refresh'
    JWT_SESSION_COOKIE = False
    JWT_COOKIE_SECURE = True
    #  JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=1)
    #  JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=10)
    MONGODB_SETTINGS = {
        'host': 'mongodb',
        'db': 'onelove',
    }
    REDIS_HOST = REDIS_HOST
    CELERY_LOG_LEVEL = 'INFO'
    CELERY_BROKER_URL = 'redis://{}:6379'.format(REDIS_HOST)
    CELERY_RESULT_BACKEND = 'redis://{}:6379'.format(REDIS_HOST)
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    JWT_COOKIE_SECURE = False
    SECURITY_SEND_REGISTER_EMAIL = False


class TestConfig(Config):
    TESTING = True
    JWT_COOKIE_SECURE = False
    MONGODB_SETTINGS = {
        'host': MONGODB_HOST,
        'db': 'onelovetest',
    }


class ProdConfig(Config):
    pass
