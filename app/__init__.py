#!/usr/bin/env python3

from logging import handlers
import logging

from flask.ext import sqlalchemy
import flask

from .. import api

flask.g.db = db = sqlalchemy.SQLAlchemy()


def app(config):
    _app = flask.Flask(__name__)
    _app.config.from_object(config)
    email_handler = handlers.SMTPHandler(app.config["EMAIL_SMTP_SERVER"],
                                         app.config["EMAIL_SENDER_ADDRESS"],
                                         app.config["EMAIL_RECIPIENT_ADDRESS"],
                                         "Failure @ "
                                         "http://www.adamcunnington.info",
                                         secure=())
    email_handler.setFormatter(logging.Formatter("Error Type: %(levelname)s\n"
                                                 "Location: %(pathname)s: "
                                                 "%(lineno)d\n"
                                                 "Module: %(module)s\n"
                                                 "Function: %(funcName)s\n"
                                                 "Time: %(asctime)s\n"
                                                 "%(message)s"))
    file_handler = handlers.FileHandler()
    file_handler.setFormatter(logging.Formatter("%(asctime)s (%(levelname)s) "
                                                "-> %(message)s "
                                                "[in %(pathname)s: "
                                                "%(lineno)d]"))
    for handler in (email_handler, file_handler):
        handler.setLevel(logging.ERROR)
    for logger in (app.logger, logging.getLogger("sqlalchemy")):
        for handler in (email_handler, file_handler):
            logger.addHandler(handler)
    db.init_app(_app)
    _app.register_blueprint(api.api, subdomain="api")
    _app.register_blueprint(api.token, url_prefix="/auth")
    return _app
