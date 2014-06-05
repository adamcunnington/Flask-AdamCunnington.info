#!/usr/bin/env python3

import flask

from . import auth, decorators, errors

api = flask.Blueprint("api", __name__)
token = flask.Blueprint("token", __name__)


@api.after_request
@token.after_request
def _after_request(response):
    try:
        response.headers.extend(flask.g.headers)
    except AttributeError:
        pass
    return response


@api.errorhandler(400)
@token.errorhandler(400)
def _bad_request_error(error):
    return errors.bad_request("invalid request")


@api.before_request
@token.before_request
@decorators.rate_limit
@auth.auth.login_required
@auth.token_auth.login_required
def _before_request():
    pass


@api.errorhandler(errors.InvalidQueryError)
@token.errorhandler(errors.InvalidQueryError)
@api.errorhandler(errors.LookupError)
@token.errorhandler(errors.LookupError)
def _lookup_error(error):
    return errors.bad_request(error.args[0])


@api.errorhandler(404)
@token.errorhandler(404)
def _not_found_error(error):
    return errors.not_found_error("invalid request")


@token.route("/request-token")
@decorators.no_cache
def _request_token():
    return flask.jsonify({"token": flask.g.user.generate_auth_token()})
