#!/usr/bin/env python3

import flask


class InvalidQueryError(Exception):
    """Invalid query parameter value(s)."""


class LookupError(Exception):
    """Data not found in the database."""


def not_modified():
    return flask.make_response(flask.jsonify({"error": "not modified"}), 304)


def bad_request(message):
    return flask.make_response(flask.jsonify({"error": "bad request",
                                              "message": message}), 400)


def unauthorised(message):
    return flask.make_response(flask.jsonify({"error": "unathorised",
                                             "message": message}), 401)


def forbidden(message):
    return flask.make_response(flask.jsonify({"error": "forbidden",
                                              "message": message}), 403)


def not_found(message):
    return flask.make_response(flask.jsonify({"error": "not found",
                                              "message": message}), 404)


def precondition_failed():
    return flask.make_response(flask.jsonify({"error": "precondition failed"}),
                               412)


def too_many_requests(message, limit=None):
    return flask.make_response(flask.jsonify({"error": "too many requests",
                                              "message": message}), 429)
