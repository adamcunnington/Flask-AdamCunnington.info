#!/usr/bin/env python3

from logging import handlers
import logging
import os

import flask


def app_factory(config):
    app = flask.Flask(__name__)
    app.config.from_object(config)
    email_handler = handlers.SMTPHandler(config.EMAIL_SMTP_SERVER,
                                         config.EMAIL_SENDER_ADDRESS,
                                         config.EMAIL_RECIPIENT_ADDRESS,
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
    email_handler.setLevel(logging.ERROR)
    file_handler = handlers.FileHandler(os.path.join(os.path.dirname(__file__),
                                                     "..", ".log"))
    file_handler.setFormatter(logging.Formatter("%(asctime)s (%(levelname)s) "
                                                "-> %(message)s "
                                                "[in %(pathname)s: "
                                                "%(lineno)d]"))
    file_handler.setLevel(logging.WARNING)
    for logger in (app.logger, logging.getLogger("sqlalchemy")):
        for handler in (email_handler, file_handler):
            logger.addHandler(handler)
    if config.USE_API:
        from .. import api
        app.register_blueprint(api.user, subdomain="api")
        app.register_blueprint(api.token)
        flask.g.db = db = api.models.db
    else:
        from flask.ext import sqlalchemy
        flask.g.db = db = sqlalchemy.SQLAlchemy()
    db.initapp(app)

    return app
