#!/usr/bin/env python3

from flask.ext import httpauth
import flask

from . import errors, models

auth = httpauth.HTTPDigestAuth()
token_auth = httpauth.HTTPDigestAuth()


@auth.error_handler
def _unauthorised_auth_error():
    return errors.unauthorised("Incorrect or expired authentication token")


@token_auth.error_handler
def _unauthorised_token_auth_error():
    return errors.unauthorised("Invalid credentials")


@auth.verify_password
def _verify_token(token):
    flask.g.user = models.APIProfile.verify_auth_token(token)
    return flask.g.user is not None


@token_auth.verify_password
def _verify_credentials(username, password):
    flask.g.user = models.APIProfile.query.filter_by(username).first()
    if not flask.g.user:
        return False
    return flask.g.user.verify_password(password)
