#!/usr/bin/env python3

import os

_base_dir_name = os.path.dirname(__file__)


class Config(object):
    DEBUG = False
    RATE_LIMIT = os.environ.get("AC_RATE_LIMIT")
    RATE_LIMIT_PERIOD = os.environ.get("AC_RATE_LIMIT_PERIOD")
    SECRET_KEY = os.environ.get("AC_SECRET_KEY") or os.urandom(24)
    TESTING = False


class DevelopmentConfig(Config):
    DB_URI = (os.environ.get("AC_DB_DEV_URI") or "sqlite:///%s" %
              os.path.join(_base_dir_name, "data-dev.sqlite"))
    DEBUG = True
    RATE_LIMIT = 10
    RATE_LIMIT_PERIOD = 15


class ProductionConfig(Config):
    DB_URI = (os.environ.get("AC_DB_URI") or "sqlite:///%s" %
              os.path.join(_base_dir_name, "data.sqlite"))


class TestingConfig(Config):
    DB_URI = (os.environ.get("AC_DB_TESTING_URI") or "sqlite:///%s" %
              os.path.join(_base_dir_name, "data-test.sqlite"))
    SECRET_KEY = "secret"
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
