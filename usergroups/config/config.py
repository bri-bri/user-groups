import logging

class Config(object):
    DEBUG = False
    LOG_LEVEL = logging.INFO
    PORT = 5000

class ProductionConfig(Config):
    LOG_LEVEL = logging.INFO

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

class TestingConfig(Config):
    TESTING = True
    LOG_LEVEL = logging.DEBUG