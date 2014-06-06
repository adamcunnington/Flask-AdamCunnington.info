#!/usr/bin/env python3

from flask.ext import sqlalchemy
import flask

from .. import api

flask.g.db = db = sqlalchemy.SQLAlchemy()


def app(config):
    _app = flask.Flask(__name__)
    _app.config.from_object(config)
    # To Do: Implement Logging
    db.init_app(_app)
    _app.register_blueprint(api.api, subdomain="api")
    _app.register_blueprint(api.token, url_prefix="/auth")
    return _app
