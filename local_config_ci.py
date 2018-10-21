from common_config import TestConfig as Config


class TestConfig(Config):
    MONGO_SETTINGS = {
        'host': 'localhost',
    }
