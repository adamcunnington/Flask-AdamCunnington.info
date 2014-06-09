#!/usr/bin/env python3

import os

_base_dir_name = os.path.dirname(__file__)


class Config(object):
    DEBUG = False
    EMAIL_SMTP_SERVER = os.environ.get("EMAIL_SMTP_SERVER")
    EMAIL_SENDER_ADDRESS = os.environ.get("EMAIL_SENDER_ADDRESS")
    EMAIL_RECIPIENT_ADDRESS = os.environ.get("EMAIL_RECIPIENT_ADDRESS")
    RATE_LIMIT = os.environ.get("AC_RATE_LIMIT")
    RATE_LIMIT_PERIOD = os.environ.get("AC_RATE_LIMIT_PERIOD")
    SECRET_KEY = os.environ.get("AC_SECRET_KEY") or os.urandom(24)
    TESTING = False
    USE_API = os.environ.get("AC_USE_API")


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = (os.environ.get("AC_DB_DEV_URI") or
                               "sqlite:///%s" %
                               os.path.join(_base_dir_name, "data-dev.sqlite"))
    DEBUG = True
    RATE_LIMIT = 10
    RATE_LIMIT_PERIOD = 15


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (os.environ.get("AC_DB_URI") or "sqlite:///%s" %
                               os.path.join(_base_dir_name, "data.sqlite"))


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = (os.environ.get("AC_DB_TEST_URI") or
                               "sqlite:///%s" %
                               os.path.join(_base_dir_name,
                                            "data-test.sqlite"))
    SECRET_KEY = "secret"
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
