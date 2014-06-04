#!/usr/bin/env python3

import flask


class LookupError(Exception):
    """Data not found in the database"""


def not_modified():
    response = flask.jsonify({"status": 304, "error": "not modified"})
    response.status_code = 304
    return response


def bad_request(message):
    response = flask.jsonify({"status": 400, "error": "bad request",
                              "message": message})
    response.status_code = 400
    return response


def unauthorised(message):
    response = flask.jsonify({"status": 401, "error": "unauthorised",
                              "message": message})
    response.status_code = 401
    return response


def forbidden(message):
    response = flask.jsonify({"status": 403, "error": "forbidden",
                              "message": message})
    response.status_code = 403
    return response


def not_found(message):
    response = flask.jsonify({"status": 404, "error": "not found",
                              "message": message})
    response.status_code = 404
    return response


def precondition_failed():
    response = flask.jsonify({"status": 412, "error": "precondition failed"})
    response.status_code = 412
    return response


def too_many_requests(message, limit=None):
    response = flask.jsonify({"status": 429, "error": "too many requests",
                              "limit": limit, "message": message})
    response.status_code = 429
    return response
